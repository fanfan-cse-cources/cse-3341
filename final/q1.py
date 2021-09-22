class Repeat:

    def parse(self, parser):
        parser.expectSingle(Core.REPEAT)
        parser.tokenizer.skipToken()
        self.ss = StmtSeq()
        self.ss.parse(parser)

        parser.expectSingle(Core.UNTIL)
        parser.tokenizer.skipToken()

        self.cond = Cond()
        self.cond.parse(parser)

        parser.expectSingle(Core.SEMICOLON)
        parser.tokenizer.skipToken()

    def execute(self, parser):
        self.ss.execute(parser)

        while self.cond.execute(parser) == False:
            self.ss.execute(parser)

    def print(self, indent):
        for x in range(indent):
            print("  ", end="")
        print("repeat ")
        self.ss.print(indent + 1)
        for x in range(indent):
            print("  ", end="")
        print("until ", end="")
        self.cond.print()
        print(";", end="")
        print()
