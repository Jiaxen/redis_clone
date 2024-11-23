# Parser for Redis serialization protocol
# Reference: https://redis.io/docs/latest/develop/reference/protocol-spec/#resp-versions
DELIMITER = "\r\n"
ARRAY_INDICATOR = "*"
BULK_STRING_INDICATOR = "$"
SIMPLE_STRING_INDICATOR = "+"

class RedisParser:

    def encode_bulk_str(self, input_str):
        print("Encoding bulk string")
        return f'{BULK_STRING_INDICATOR}{len(input_str)}{DELIMITER}{input_str}{DELIMITER}'.encode()

    def encode_simple_str(self, input_str):
        print("Encoding simple string")
        return f'{SIMPLE_STRING_INDICATOR}{input_str}{DELIMITER}'.encode()

    def decode(self, input_str):
        print("Decoding input")
        input_str = input_str.decode()
        first_char = input_str[0]
        if first_char == ARRAY_INDICATOR:
            return self.parse_array_of_bulk_str(input_str)
        return self.parse_default(input_str)

    def parse_default(self, input_str):
        return input_str.split(DELIMITER)

    def parse_array_of_bulk_str(self, bulk_array: str):
        print("Parsing bulk string array")
        if bulk_array[0] != ARRAY_INDICATOR:
            raise ValueError(f"Input {bulk_array} does not begin with array indicator {ARRAY_INDICATOR}")
        index = bulk_array.find(DELIMITER)
        array_len = int(bulk_array[1:index])
        result = []
        for i in range(array_len):
            index += len(DELIMITER)
            bulk_element, index = self.parse_bulk_str(bulk_array, index)
            result.append(bulk_element)
        return result

    def parse_bulk_str(self, bulk_str: str, start_index=0):
        print("Parsing bulk string")
        if bulk_str[start_index] != BULK_STRING_INDICATOR:
            raise ValueError(f"{bulk_str} does not contain input indicator {BULK_STRING_INDICATOR} at index {start_index}")
        index = bulk_str.find(DELIMITER, start_index)
        bulk_string_len = int(bulk_str[start_index + 1:index])
        if bulk_string_len <= 0:
            return None, index + len(DELIMITER)
        result = bulk_str[index + len(DELIMITER):index + len(DELIMITER) + bulk_string_len]
        return result, index + len(DELIMITER) + bulk_string_len

