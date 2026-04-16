#!/usr/bin/env python3
"""
Apply English translations to en/*.html (bulk string replacement).
Longest keys first to avoid partial overlaps.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (Chinese/mixed, English) — order here is sorted by length descending before apply
RAW_PAIRS: list[tuple[str, str]] = [
    # Meta / UI
    ('<html lang="zh-CN">', '<html lang="en">'),
    ('aria-label="周次导航"', 'aria-label="Course weeks"'),
    ('title="Week 1 思维导图"', 'title="Week 1 mind map"'),
    ('"✅ Aggregation — 聚合表示 part-whole（部分与整体）关系，部分可独立存在于整体之外，正是本题答案。"', '"✅ Aggregation — Aggregation models part-whole: parts can exist outside the whole; this is the correct answer."'),
    ('"❌ None of the above — 错误，Aggregation 正是正确答案。"', '"❌ None of the above — Wrong; Aggregation is correct."'),
    # Week 1 notes — full sentences
    ('SDLC 是软件从无到有、从发布到维护的完整生命周期框架，定义了开发过程中每个阶段的任务与目标。', 'The SDLC is the full life-cycle framework from inception through release and maintenance, defining tasks and goals for each phase.'),
    ('<tr><th>阶段</th><th>核心任务</th><th>产出物</th></tr>', '<tr><th>Phase</th><th>Main tasks</th><th>Artifacts</th></tr>'),
    ('<td>收集、分析用户需求</td>', '<td>Gather and analyze user needs</td>'),
    ('<td>规划架构、模块、接口</td>', '<td>Plan architecture, modules, interfaces</td>'),
    ('<td>编码开发</td>', '<td>Implementation / coding</td>'),
    ('<td>验证功能与质量</td>', '<td>Verify functionality and quality</td>'),
    ('<td>修复 bug、迭代更新</td>', '<td>Fix bugs and ship updates</td>'),
    ('<td>需求规格说明书 (SRS)</td>', '<td>Software Requirements Specification (SRS)</td>'),
    ('<td>设计文档、UML 图</td>', '<td>Design docs, UML diagrams</td>'),
    ('<td>源代码</td>', '<td>Source code</td>'),
    ('<td>测试报告</td>', '<td>Test reports</td>'),
    ('<td>补丁、新版本</td>', '<td>Patches, new releases</td>'),
    ('<div class="note-label">考点提示</div>', '<div class="note-label">Exam tip</div>'),
    ('<strong>Evaluation Phase 不属于 SDLC 标准阶段。</strong> 常见干扰项，注意区分。', '<strong>Evaluation Phase is not a standard SDLC phase.</strong> Common distractor—know the difference.'),
    ('<div class="card-title">The Trinity of Software Project（软件项目三元组）</div>', '<div class="card-title">The Trinity of a Software Project</div>'),
    ('软件项目由三个核心要素构成，缺少任一要素都不完整。三者相互依存、共同决定项目成败。', 'A software project rests on three pillars; omit any one and the picture is incomplete. They depend on one another and together determine success or failure.'),
    ('<div class="sc-val">最终交付的软件产品本身</div>', '<div class="sc-val">The delivered software product itself</div>'),
    ('<div class="sc-val">使用该系统的人群</div>', '<div class="sc-val">People who use the system</div>'),
    ('<div class="sc-val">构建软件所用的方法与流程</div>', '<div class="sc-val">The methods and process used to build the software</div>'),
    ('<strong>Software Design 不在三元组内。</strong> Design 是开发过程中的一个阶段，而非独立的三元组成员。', '<strong>Software Design is not part of the trinity.</strong> Design is a phase of development, not a separate pillar.'),
    ('<div class="card-title">Information Hiding（信息隐藏）</div>', '<div class="card-title">Information Hiding</div>'),
    ('将组件的<span class="hl">内部实现细节</span>隐藏起来，只对外暴露<span class="hl-blue">接口 (Interface)</span>。当内部设计变更时，外部调用方代码无需修改。', 'Hide a component’s <span class="hl">internal implementation</span> and expose only its <span class="hl-blue">interface</span>. When internals change, external code does not need to change.'),
    ('<li>修改内部逻辑 → 外部代码不受影响</li>', '<li>Change internals → external code stays unaffected</li>'),
    ('<li>提升模块独立性，降低耦合度 (coupling)</li>', '<li>Improves modularity and lowers coupling</li>'),
    ('<li>是 OOP 中 Encapsulation（封装）的核心思想</li>', '<li>Core idea behind encapsulation in OOP</li>'),
    ('<thead><tr><th>概念</th><th>重点</th></tr></thead>', '<thead><tr><th>Concept</th><th>Focus</th></tr></thead>'),
    ('<tr><td>Information Hiding</td><td>隐藏内部决策，对外只暴露接口</td></tr>', '<tr><td>Information Hiding</td><td>Hide internals; expose the interface</td></tr>'),
    ('<tr><td>Divide and Conquer</td><td>把大问题拆分成小问题分别解决</td></tr>', '<tr><td>Divide and Conquer</td><td>Split big problems into smaller ones</td></tr>'),
    ('<tr><td>Inheritance</td><td>子类复用父类属性与方法（OOP 机制）</td></tr>', '<tr><td>Inheritance</td><td>Subclass reuses parent fields/methods (OOP)</td></tr>'),
    ('<tr><td>Project Management</td><td>计划、组织、控制项目执行</td></tr>', '<tr><td>Project Management</td><td>Plan, organize, and control execution</td></tr>'),
    ('<div class="card-title">Software 的核心特征：Malleable（可塑性）</div>', '<div class="card-title">Key characteristic of software: Malleable</div>'),
    ('软件最显著的特征是<span class="hl-green">高度可塑性 (Malleable)</span>——可以被轻易修改、扩展、重构，这是与硬件最大的不同。', 'Software’s hallmark is <span class="hl-green">malleability</span>—it can be changed, extended, and refactored far more easily than hardware.'),
    ('<thead><tr><th>特征</th><th>说明</th><th>正确？</th></tr></thead>', '<thead><tr><th>Trait</th><th>Meaning</th><th>Correct?</th></tr></thead>'),
    ('<td style="color:var(--accent);font-weight:600;">✓ 正确</td>', '<td style="color:var(--accent);font-weight:600;">✓ True</td>'),
    ('<td style="color:var(--red);font-weight:600;">✗ 错误</td>', '<td style="color:var(--red);font-weight:600;">✗ False</td>'),
    ('<td>易于修改与调整</td>', '<td>Easy to change</td>'),
    ('<td>现实中软件高度复杂</td>', '<td>Real software is highly complex</td>'),
    ('<td>软件持续演进，非恒定不变</td>', '<td>Software evolves; it is not fixed</td>'),
    ('<td>现实软件通常需要团队协作</td>', '<td>Real software usually needs teams</td>'),
    ('<div class="card-title">Brooks\' Law — 增人不增速</div>', '<div class="card-title">Brooks’ Law — more people, not faster</div>'),
    ('<li>新成员需要<strong>上手时间 (onboarding)</strong>，短期内不产出</li>', '<li>New hires need <strong>onboarding</strong> time and produce little at first</li>'),
    ('<li>人员增加 → 沟通路径指数级增长 → <strong>communication overhead</strong> 急剧上升</li>', '<li>More people → communication paths grow → <strong>communication overhead</strong> spikes</li>'),
    ('<li>老成员被迫分心辅导新人 → 整体效率下降</li>', '<li>Veterans mentor newcomers → overall throughput drops</li>'),
    ('<div class="note-label">一句话总结</div>', '<div class="note-label">In short</div>'),
    ('增加团队人数不能解决 Software Crisis，反而可能使情况更糟。', 'Adding people does not fix the software crisis; it often makes things worse.'),
    ('<div class="card-title">Project Stakeholders（项目利益相关方）</div>', '<div class="card-title">Project Stakeholders</div>'),
    ('所有对软件项目有利益关联或影响的人，统称为 <span class="hl-blue">Stakeholders</span>。范围远比"开发者"更广。', 'Everyone with an interest in or impact on the project is a <span class="hl-blue">stakeholder</span>—far beyond “developers” alone.'),
    ('<thead><tr><th>角色</th><th>描述</th></tr></thead>', '<thead><tr><th>Role</th><th>Description</th></tr></thead>'),
    ('<tr><td>Customer</td><td>付费购买/委托开发软件的人或组织</td></tr>', '<tr><td>Customer</td><td>Pays for or commissions the software</td></tr>'),
    ('<tr><td>User</td><td>实际使用软件的人（可与 Customer 不同）</td></tr>', '<tr><td>User</td><td>Actually uses the software (may differ from Customer)</td></tr>'),
    ('<tr><td>Designer</td><td>负责系统架构与界面设计</td></tr>', '<tr><td>Designer</td><td>System and UI design</td></tr>'),
    ('<tr><td>Tester</td><td>验证软件质量与功能正确性</td></tr>', '<tr><td>Tester</td><td>Checks quality and correctness</td></tr>'),
    ('<tr><td>Support Engineer</td><td>负责部署、运维与用户支持</td></tr>', '<tr><td>Support Engineer</td><td>Deploys, operates, and supports users</td></tr>'),
    ('<tr><td>Project Manager</td><td>协调资源、进度与风险</td></tr>', '<tr><td>Project Manager</td><td>Coordinates resources, schedule, risk</td></tr>'),
    ('<li><strong>Customer</strong>：出钱的人，如企业采购方</li>', '<li><strong>Customer</strong>: who pays (e.g. procurement)</li>'),
    ('<li><strong>User</strong>：用软件的人，如企业员工</li>', '<li><strong>User</strong>: who uses the software (e.g. staff)</li>'),
    ('<li>两者可以是同一人，也可以完全不同（常见于 B2B 场景）</li>', '<li>They may be the same person or not (common in B2B)</li>'),
    ('<div class="note-label">例子</div>', '<div class="note-label">Example</div>'),
    ('公司 IT 部门购买了一款 CRM 软件（Customer = IT 部门），实际使用的是销售团队（Users = 销售人员）。', 'The IT department buys a CRM (Customer = IT); the sales team uses it (Users = sales).'),
    ('<thead><tr><th></th><th>Programming（编程）</th><th>Software Engineering（软件工程）</th></tr></thead>', '<thead><tr><th></th><th>Programming</th><th>Software Engineering</th></tr></thead>'),
    ('<tr><td>规模</td><td>个人或小脚本</td><td>Multi-person 团队协作</td></tr>', '<tr><td>Scale</td><td>Individual or small scripts</td><td>Multi-person team effort</td></tr>'),
    ('<tr><td>版本</td><td>通常单一版本</td><td>Multi-version，持续演进</td></tr>', '<tr><td>Versions</td><td>Often a single version</td><td>Many versions, continuous evolution</td></tr>'),
    ('<tr><td>寿命</td><td>短期、临时</td><td>长期维护（Long-lived）</td></tr>', '<tr><td>Lifetime</td><td>Short-term, ad hoc</td><td>Long-lived maintenance</td></tr>'),
    ('<tr><td>关注点</td><td>让代码跑起来</td><td>流程、设计、质量、协作</td></tr>', '<tr><td>Focus</td><td>Make code run</td><td>Process, design, quality, teamwork</td></tr>'),
    ('<tr><td>产出</td><td>可运行程序</td><td>可维护的软件系统</td></tr>', '<tr><td>Output</td><td>A running program</td><td>A maintainable software system</td></tr>'),
    ('<li>SE 包含编程，但远不止编程——还涉及需求、设计、测试、维护等全流程</li>', '<li>SE includes coding but also requirements, design, testing, maintenance, …</li>'),
    ('<li>SE 的核心挑战是在<strong>多人协作、长期演进</strong>的背景下保持质量与一致性</li>', '<li>Core challenge: keep quality and consistency under <strong>teamwork and long-term change</strong></li>'),
    ('<div class="note-label">软件工程师的关键属性</div>', '<div class="note-label">Key trait of software engineers</div>'),
    ('除了技术能力，还需具备 <strong>ability to efficiently/effectively interact and work in a team</strong>——团队协作能力是软件工程师区别于单纯程序员的核心素质。', 'Beyond technical skill, you need <strong>the ability to interact and work effectively in a team</strong>—that collaboration is what distinguishes engineers from “code-only” programmers.'),
    ('<div class="card-title">Competing Goals of Software Project（竞争性目标）</div>', '<div class="card-title">Competing Goals of a Software Project</div>'),
    ('软件项目的三大竞争性目标相互制约，通常无法同时最优——即项目管理中的 <span class="hl-amber">"Iron Triangle"</span>（铁三角）。', 'Time, cost, and quality trade off—you rarely optimize all three. This is the <span class="hl-amber">Iron Triangle</span>.'),
    ('<div class="sc-label">Time（时间）</div>', '<div class="sc-label">Time</div>'),
    ('<div class="sc-val">开发者用于开发的时间与项目周期</div>', '<div class="sc-val">Schedule and calendar time for development</div>'),
    ('<div class="sc-label">Cost（成本）</div>', '<div class="sc-label">Cost</div>'),
    ('<div class="sc-val">客户支付给团队的开发费用</div>', '<div class="sc-val">What the customer pays the team</div>'),
    ('<div class="sc-label">Quality（质量）</div>', '<div class="sc-label">Quality</div>'),
    ('<div class="sc-val">软件的功能完整性与可靠性</div>', '<div class="sc-val">Functional completeness and reliability</div>'),
    ('<li>想要<strong>更快</strong>交付 → 需要增加成本 或 降低质量</li>', '<li>Faster delivery → spend more or cut quality</li>'),
    ('<li>想要<strong>更便宜</strong> → 需要延长时间 或 降低质量</li>', '<li>Lower cost → take longer or cut quality</li>'),
    ('<li>想要<strong>更高质量</strong> → 需要更多时间 或 更高成本</li>', '<li>Higher quality → more time or more money</li>'),
    ('<div class="card-body"><span class="hl">不属于</span>竞争性目标的选项：</div>', '<div class="card-body">Options that <span class="hl">do not</span> belong among competing goals:</div>'),
    ('<strong>Market share（市场占有率）</strong>是业务/商业指标，<strong>不属于</strong>软件项目的 competing goals。Time、Cost、Quality 才是三大核心竞争目标。', '<strong>Market share</strong> is a business metric, <strong>not</strong> a competing goal of the project in this sense. Time, Cost, and Quality are the three.'),
    # Tab buttons week 1
    ('onclick="switchTab(\'concepts\',this)">核心概念</button>', 'onclick="switchTab(\'concepts\',this)">Core concepts</button>'),
    ('onclick="switchTab(\'se\',this)">SE vs. 编程</button>', 'onclick="switchTab(\'se\',this)">SE vs. programming</button>'),
]

def pairs_sorted() -> list[tuple[str, str]]:
    return sorted(RAW_PAIRS, key=lambda x: len(x[0]), reverse=True)


def translate_file(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    orig = text
    for zh, en in pairs_sorted():
        if zh in text:
            text = text.replace(zh, en)
    if text != orig:
        path.write_text(text, encoding='utf-8')
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def main() -> None:
    total = 0
    for p in sorted(ROOT.glob('en/*.html')):
        left = translate_file(p)
        total += left
        print(f'{p.name}: {left} CJK chars remaining')
    print('TOTAL CJK remaining:', total)


if __name__ == '__main__':
    main()
