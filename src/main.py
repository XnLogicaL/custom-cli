import os, sys
from bcolors import bcolors
from platform import python_version

class main:
    def __init__(self):
        self.running = True
        self.version = 0.1

        self.run()

    def err(self, s):
        print(bcolors.wrap(s, bcolors.FAIL))

    def warn(self, s):
        print(bcolors.wrap(s, bcolors.WARNING))

    def first_numeric_index(self, d: dict):
        for i in range(len(list(d))):
            key = list(d.keys())[i]
            if str(key).isnumeric():
                return key
        return None
        
    def parse_args(self, args):
        parsed = {}
        for i, arg in enumerate(args):
            if arg.startswith("--"):
                if i == len(args):
                    continue
                parsed[arg.replace("--", "")] = True
            else:
                parsed[i] = arg
        return parsed

    def run(self):
        while self.running:
            cmd = ""
            try:
                cmd = input("clic >> ")
            except KeyboardInterrupt:
                print("\nuse 'exit' to quit clic"),
                continue

            args = cmd.split(" ")
            header = args.pop(0)
            parsed_args = self.parse_args(args) 

            match header:
                case "exit":
                    self.running = False
                    break
                case "argdbg":
                    print(parsed_args)

                case "internal":
                    if not (parsed_args.get("version") is None):
                        self.warn(f"clic {self.version}")
                    elif not (parsed_args.get("pyversion") is None):
                        self.warn(f"Python {python_version()}")
                    else:
                        self.err("invalid sub argument")

                case "python3":
                    while True:
                        src = input("python3 >> ")
                        match src:
                            case "exit":
                                break
                            case _:
                                try:
                                    print(eval(src))
                                except Exception as e:
                                    self.err(e)

                case "mkdir":
                    try:
                        os.mkdir(parsed_args.get(self.first_numeric_index(parsed_args)))
                    except Exception as e:
                        self.err(f"mkdir failed (exit code {e})")
                case "rm":
                    path = parsed_args.get(self.first_numeric_index(parsed_args))
                    force_mode = parsed_args["force"]
                    try:
                        if force_mode and bool(force_mode):
                            while os.path.exists(path):
                                os.remove(path)
                        else:
                            os.remove(path)
                    except Exception as e:
                        self.err(f"rm failed (exit code {e})")
                case "rd":
                    try:
                        print(f"\n{open(parsed_args.get(self.first_numeric_index(parsed_args))).read()}\n")
                    except Exception as e:
                        self.err(f"rd failed (exit code {e})")

                case _:
                    if header != "":
                        self.err(f"'{header}' is not an internally recognized command")

if __name__ == "__main__":
    main()
