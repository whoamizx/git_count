import os
import subprocess

repo_path = input("请输入你想分析的 Git 仓库路径：").strip()
author = input("请输入你的 Git 名或邮箱：").strip()

if not os.path.isdir(repo_path) or not os.path.isdir(os.path.join(repo_path, ".git")):
    print("❌ 不是有效的 Git 仓库路径")
    exit(1)

cmd = [
    "git",
    f"--git-dir={os.path.join(repo_path, '.git')}",
    f"--work-tree={repo_path}",
    "log",
    f"--author={author}",
    "--pretty=tformat:%ad",
    "--date=short",
    "--numstat"
]

with open("log.txt", "w") as f:
    subprocess.run(cmd, stdout=f)

print("✅ log.txt 已生成")
