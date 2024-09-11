from token import OP
from pydantic import BaseModel, Field, computed_field, ValidationError
import json, re
from typing import List, Optional

class BashCode(BaseModel):
    instructions: str = Field(description='User instructions that require bash code')
    modifications: Optional[str] = Field(default=None, description="User modifications to implement if given for the bash code")
    stepwise_bash_code: List[str] = Field(default_factory=list, description="list of Bash codes that has to run sequentially to complete the user's intended task")
    warnings: Optional[str] = Field(default=None, description='Warning that tells what running this code can cause')
    permission_required: bool = Field(default=True, description="Ask for user's permission if the code is potentially harmful or can cause any loss")

    # This line is necessary to resolve forward references in Pydantic
    class Config:
        arbitrary_types_allowed = True  
        
    class Config:
        arbitrary_types_allowed = True  
    
    @classmethod
    def from_text(cls, text: str):
        """
        Extracts the JSON object from the given text, specifically looking for
        JSON enclosed in ```json and ``` tags. If JSON parsing fails, it falls
        back to extracting fields using regex from the found JSON string.

        Args:
        text (str): The input text containing JSON.

        Returns:
        BashCode: An instance of the BashCode class populated with the extracted JSON data.
        None: If extraction fails entirely.
        """
        # Extract JSON block with regex
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)

        if json_match:
            json_str = json_match.group(1)
            try:
                # Attempt to parse the JSON
                json_obj = json.loads(json_str)

                # Validate and parse JSON into the BashCode model
                return cls(**json_obj)

            except (json.JSONDecodeError, ValidationError) as e:
                print(f"JSON parsing failed. Attempting to extract fields manually from the found JSON string. Error: {e}")

                # Use regex to extract fields within the found JSON string
                instructions = re.search(r'"instructions":\s*"([^"]*)"', json_str)
                modifications = re.search(r'"modifications":\s*"([^"]*)"', json_str)
                stepwise_bash_code = re.findall(r'"stepwise_bash_code":\s*\[(.*?)\]', json_str, re.DOTALL)
                warnings = re.search(r'"warnings":\s*"([^"]*)"', json_str)
                permission_required = re.search(r'"permission_required":\s*(true|false)', json_str, re.IGNORECASE)

                # Clean and parse the extracted stepwise bash code if found
                if stepwise_bash_code:
                    # Extract each bash code inside the list
                    bash_code_list = re.findall(r'"([^"]*)"', stepwise_bash_code[0])
                else:
                    bash_code_list = []

                # Create the BashCode object with extracted values
                return cls(
                    instructions=instructions.group(1) if instructions else "",
                    modifications=modifications.group(1) if modifications else None,
                    stepwise_bash_code=bash_code_list,
                    warnings=warnings.group(1) if warnings else None,
                    permission_required=permission_required.group(1).lower() == 'true' if permission_required else True
                )

        # If no JSON block is found, return None
        print("No JSON block found in the text.")
        return None



class CodeReport(BaseModel):
    code: str
    run:bool=False
    stdout: Optional[str] = Field(default=None, description='Terminal output of ran bash code')
    stderr: Optional[str] = Field(default=None, description='Terminal error output of ran bash code')
    exit_code:Optional[int] = Field(default=0, description='Exit code got from running the code')

class BashCodeRun(BashCode):
    previous_runs: Optional[List['BashCodeRun']] = Field(default=None, description='Previous runs of commands that resulted in an error')
    logs: list[CodeReport] =Field(discription ='report of each code lines, contains code, if ran or not, and output , error ')

    
    @computed_field
    def error(self) -> bool:
        for log in self.logs:
            if log.exit_code != 0:
                return True
        else:
            return False
    
    def get_logs_str(self):
        logs = ''
        for log in self.logs:
            logs += str(log.model_dump())
        return logs
        
# text = '''
# Here's a step-by-step thought process to solve the problem:

# **Understand the task:**
# The main objective is to find the top 5 biggest files inside the `/home/t/Downloads` folder, considering all subfolders.

# **Break down the task:**
# Step 1: Use the `find` command to search for all files recursively in the `/home/t/Downloads` folder.
# Step 2: Sort the files based on their size in descending order.
# Step 3: Show the top 5 files.

# **Develop bash code for each step:**

# Step 1: Find all files recursively
# ```bash
# find /home/t/Downloads -type f
# ```
# This command will find all files in the `/home/t/Downloads` folder and its subfolders.

# Step 2: Sort files by size
# ```bash
# find /home/t/Downloads -type f -exec stat -c "%s %n" {} \; | sort -rn | cut -d" " -f1-2
# ```
# This command uses `stat` to get the file size and name, then pipes the output to `sort` to sort the files by size in descending order. `cut` is used to extract the file size and name from the output.

# Step 3: Show top 5 files
# ```bash
# find /home/t/Downloads -type f -exec stat -c "%s %n" {} \; | sort -rn | cut -d" " -f1-2 | head -5
# ```
# This command combines the previous two steps and limits the output to the top 5 files.

# **Final output in JSON schema:**

# ```json
# {
#   "instructions": "Find the top 5 biggest files in the /home/t/Downloads folder, considering all subfolders.",
#   "modifications": "",
#   "stepwise_bash_code": [
#     "find /home/t/Downloads -type f",
#     "find /home/t/Downloads -type f -exec stat -c \"%s %n\" {} \; | sort -rn | cut -d\" \" -f1-2",
#     "find /home/t/Downloads -type f -exec stat -c \"%s %n\" {} \; | sort -rn | cut -d\" \" -f1-2 | head -5"
#   ],
#   "warnings": "This script may take some time to execute, especially if you have a large number of files. Make sure you have sufficient disk space and RAM.",
#   "permission_required": true
# }
# ```
# '''

# a = BashCode.from_text(text=text)

# print('++++++++++++++++++++++++++++')
# print(a)