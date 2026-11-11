#!/usr/bin/env python3
"""AI 日报全流程：采集 → 选题雷达 → 主笔 → 文字编辑（最多退回 2 轮）→ 视觉排版 → 关卡 → （可选）推送。
Usage:
  python3 pipeline/run.py [--date YYYY-MM-DD] [--push] [--from STAGE]
  STAGE: collect | radar | writer | editor | designer | check
Without --push nothing leaves the machine. Exit code 1 when the gate (scripts/check.py) fails.
"""
import argparse, datetime as dt, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import collect, roles, llm
from roles import P

STAGES = ['collect', 'radar', 'writer', 'editor', 'designer', 'check']

def sh(*cmd, check=True):
    print('$', ' '.join(cmd)); return subprocess.run(cmd, cwd=roles.ROOT, check=check)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', default=dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime('%Y-%m-%d'))
    ap.add_argument('--push', action='store_true')
    ap.add_argument('--from', dest='start', default='collect', choices=STAGES)
    ap.add_argument('--to', dest='stop', default=STAGES[-1], choices=STAGES)
    a = ap.parse_args(); day = a.date
    if llm.PROVIDER == 'gemini' and not llm.KEY:
        sys.exit('缺少 GEMINI_API_KEY：请在仓库 Settings → Secrets and variables → Actions 的 Repository secrets 里添加（名字必须完全一致）')
    wdir = P('work', day); os.makedirs(wdir, exist_ok=True)
    go = lambda s: STAGES.index(a.start) <= STAGES.index(s) <= STAGES.index(a.stop)
    t0 = time.time()

    if go('collect'):
        raw = collect.collect(day, wdir)
    else:
        raw = json.load(open(os.path.join(wdir, 'raw_sources.json')))
    if go('radar'):
        rdr = roles.radar(day, raw, wdir)
    else:
        rdr = json.load(open(os.path.join(wdir, 'radar.json')))
    if go('writer'):
        roles.writer(day, rdr, wdir)
    if go('editor'):
        verdict = 'REVISE'
        for rnd in (1, 2, 3):
            verdict, issues, images = roles.editor(day, wdir, rnd)
            if verdict == 'PASS' or rnd == 3: break
            roles.revise(day, wdir, issues, images, rnd)
        if verdict != 'PASS':
            print('编辑 2 轮退回后仍未通过，停止。见 work/%s/review.md' % day); sys.exit(1)
    if go('designer'):
        lay = roles.designer(day, wdir)
        if not lay.get('ok'):
            print('排版检查没过，停止（不推送）。见 work/%s/notes.md' % day); sys.exit(1)
    print(f'[run] {time.time() - t0:.0f}s, LLM {llm.USAGE}')
    if not go('check'):
        return
    gate = sh(sys.executable, 'scripts/check.py', day, check=False)
    if gate.returncode != 0:
        sys.exit(1)
    if a.push:
        d = json.load(open(P('data', f'{day}.json')))
        sh('git', 'add', '-A')
        sh('git', 'commit', '-m', f'AI 日报 {day}：{d["title"]}', check=False)
        for ref in ('main', 'main:gh-pages'):
            if sh('git', 'push', 'origin', ref, check=False).returncode != 0:
                sh('git', 'pull', '--rebase', 'origin', 'main'); sh('git', 'push', 'origin', ref)
        print(f'pushed: https://emotionalronan.github.io/ai-daily-report/reports/{day}/')

if __name__ == '__main__':
    main()
