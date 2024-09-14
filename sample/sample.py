# this is a sample file , this is how output of llms should be
text = """
Here's a step-by-step thought process to solve the problem:

**Understand the task:**
The main objective is to find the top 5 biggest files inside the `/home/t/Downloads` folder, considering all subfolders.

**Break down the task:**
Step 1: Use the `find` command to search for all files recursively in the `/home/t/Downloads` folder.
Step 2: Sort the files based on their size in descending order.
Step 3: Show the top 5 files.

**Develop bash code for each step:**

Step 1: Find all files recursively
```bash
find /home/t/Downloads -type f
```
This command will find all files in the `/home/t/Downloads` folder and its subfolders.

Step 2: Sort files by size
```bash
find /home/t/Downloads -type f -exec stat -c "%s %n" {} \; | sort -rn | cut -d" " -f1-2
```
This command uses `stat` to get the file size and name, then pipes the output to `sort` to sort the files by size in descending order. `cut` is used to extract the file size and name from the output.

Step 3: Show top 5 files
```bash
find /home/t/Downloads -type f -exec stat -c "%s %n" {} \; | sort -rn | cut -d" " -f1-2 | head -5
```
This command combines the previous two steps and limits the output to the top 5 files.

**Final output in JSON schema:**

```json
{
  "instructions": "Find the top 5 biggest files in the /home/t/Downloads folder, considering all subfolders.",
  "modifications": "",
  "stepwise_bash_code": [
    "find /home/t/Downloads -type f",
    "find /home/t/Downloads -type f -exec stat -c \"%s %n\" {} \; | sort -rn | cut -d\" \" -f1-2",
    "find /home/t/Downloads -type f -exec stat -c \"%s %n\" {} \; | sort -rn | cut -d\" \" -f1-2 | head -5"
  ],
  "warnings": "This script may take some time to execute, especially if you have a large number of files. Make sure you have sufficient disk space and RAM.",
  "permission_required": true
}
```
"""
