from token import OP
from pydantic import BaseModel, Field, computed_field, ValidationError
import json, re
from pathlib import Path
from typing import List, Optional
from cli.config import config_folder


class MyBaseModel(BaseModel):
    log_file: str | Path | None = Field(
        default=None, description="a jsonl file path to log"
    )

    def write_log(self, file_name: str | Path = None):
        """Writes the class to a file"""
        if not file_name:
            file_name = self.log_file

        with open(file_name, "a") as f:
            json.dump(self.model_dump_json(), f)
            f.write("\n")  # Add a newline to separate JSON objects


class BashCode(MyBaseModel):
    instructions: str = Field(description="User instructions that require bash code")
    modifications: Optional[str] = Field(
        default=None,
        description="User modifications to implement if given for the bash code",
    )
    stepwise_bash_code: List[str] = Field(
        default_factory=list,
        description="list of Bash codes that has to run sequentially to compllog_fileete the user's intended task",
    )
    warnings: Optional[str] = Field(
        default=None, description="Warning that tells what running this code can cause"
    )
    permission_required: bool = Field(
        default=True,
        description="Ask for user's permission if the code is potentially harmful or can cause any loss",
    )

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
        json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)

        if json_match:
            json_str = json_match.group(1)
            try:
                # Attempt to parse the JSON
                json_obj = json.loads(json_str)
                # Validate and parse JSON into the BashCode model
                return cls(**json_obj)
            except (json.JSONDecodeError, ValidationError) as e:
                print(
                    f"JSON parsing failed. Attempting to extract fields manually. Error: {e}"
                )
                print("Response to be parsed as JSON: ", json_str)

                # Define a helper function to extract value between two keys
                def extract_between_keys(start_key, end_key):
                    pattern = f'"{start_key}":\\s*(.*?)(?="{end_key}":|}}\\s*$)'
                    match = re.search(pattern, json_str, re.DOTALL)
                    if match:
                        value = match.group(1).strip()
                        # Remove surrounding quotes and unescape inner quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1].replace('\\"', '"')
                        return value
                    return None

                # Extract fields
                instructions = extract_between_keys("instructions", "modifications")
                modifications = extract_between_keys(
                    "modifications", "stepwise_bash_code"
                )
                warnings = extract_between_keys("warnings", "permission_required")

                # Extract stepwise_bash_code
                stepwise_match = re.search(
                    r'"stepwise_bash_code":\s*(.*?)(?=,"warnings":)',
                    json_str,
                    re.DOTALL,
                )
                if stepwise_match:
                    stepwise_content = stepwise_match.group(1).strip()
                    # Remove the opening and closing brackets of the array
                    stepwise_content = stepwise_content.strip("[]")
                    # Split the content by commas, but not within quotes
                    stepwise_bash_code = re.findall(
                        r'"((?:[^"\\]|\\.)*)"', stepwise_content
                    )
                    # Unescape any escaped quotes within the commands
                    stepwise_bash_code = [
                        cmd.replace('\\"', '"') for cmd in stepwise_bash_code
                    ]
                else:
                    stepwise_bash_code = []

                # Extract permission_required
                permission_required = re.search(
                    r'"permission_required":\s*(true|false)', json_str, re.IGNORECASE
                )

                # Create the BashCode object with extracted values
                return cls(
                    instructions=instructions or "",
                    modifications=modifications,
                    stepwise_bash_code=stepwise_bash_code,
                    warnings=warnings,
                    permission_required=(
                        permission_required.group(1).lower() == "true"
                        if permission_required
                        else True
                    ),
                )

        # If no JSON block is found, return None
        print("No JSON block found in the text.")
        return None


class CodeReport(MyBaseModel):
    code: str
    run: bool = False
    stdout: Optional[str] = Field(
        default=None, description="Terminal output of ran bash code"
    )
    stderr: Optional[str] = Field(
        default=None, description="Terminal error output of ran bash code"
    )
    exit_code: Optional[int] = Field(
        default=0, description="Exit code got from running the code"
    )


class BashCodeRun(BashCode):
    # previous_runs: List['BashCodeRun'] |None = Field(default=None, description='Previous runs of commands that resulted in an error')
    logs: list[CodeReport] | None = Field(
        default=None,
        discription="report of each code lines, contains code, if ran or not, and output , error ",
    )
    log_file: Optional[Path] = Path(config_folder) / "bash_code_runs.jsonl"

    @computed_field
    def error(self) -> bool:
        for log in self.logs:
            if log.exit_code != 0:
                return True
        else:
            return False

    def get_logs_str(self):
        logs = ""
        for log in self.logs:
            logs += str(log.model_dump())
        return logs

    def previous_runs(self) -> List["BashCodeRun"]:
        """Reads the log_file jsonl and returns as list of dicts"""
        results = []
        if not self.log_file.exists():
            print(f"Log file {self.log_file} does not exist.")
            return results

        with open(self.log_file, "r") as f:
            for line_number, line in enumerate(f, 1):
                try:
                    line = line.strip()
                    # print('lie: ',line)
                    # print('type of line: ',type(line))

                    if line:  # Skip empty lines
                        data = json.loads(line)
                        # print('data: ', data)
                        # print('data type: ',type(data))
                        results.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON on line {line_number}: {e}")
                    print(f"Problematic line content: {line}")
                    continue  # Skip this line and continue with the next

        result_dict = []
        for result in results:
            if isinstance(result, str):
                try:
                    result_dict.append(json.loads(result))
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON on line {line_number}: {e}")
                    continue
        #     print()
        return [BashCodeRun(**result) for result in result_dict]

    def str_to_dict(self, text: str):
        return json.loads(text)
