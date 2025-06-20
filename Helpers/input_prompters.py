from Helpers.input_validators import InputValidators

class InputPrompters:

    @staticmethod
    def prompt_until_valid(prompt_msg: str, validate_func, error_msg: str, *args) -> str:
        while True:
            value = input(prompt_msg).strip()
            if value.lower() == 'exit':
                return None
            if '\0' in value or '\x00' in value:
                print("Input contains forbidden null byte characters. Please try again.")
                continue
            if validate_func(value, *args) if args else validate_func(value):
                return value
            print(error_msg)


   