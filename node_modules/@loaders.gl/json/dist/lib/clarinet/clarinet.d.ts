export type ClarinetEvent = 'onvalue' | 'onstring' | 'onkey' | 'onopenobject' | 'oncloseobject' | 'onopenarray' | 'onclosearray' | 'onerror' | 'onend' | 'onready';
declare enum STATE {
    BEGIN = 0,
    VALUE = 1,
    OPEN_OBJECT = 2,
    CLOSE_OBJECT = 3,
    OPEN_ARRAY = 4,
    CLOSE_ARRAY = 5,
    TEXT_ESCAPE = 6,
    STRING = 7,
    BACKSLASH = 8,
    END = 9,
    OPEN_KEY = 10,
    CLOSE_KEY = 11,
    TRUE = 12,
    TRUE2 = 13,
    TRUE3 = 14,
    FALSE = 15,
    FALSE2 = 16,
    FALSE3 = 17,
    FALSE4 = 18,
    NULL = 19,
    NULL2 = 20,
    NULL3 = 21,
    NUMBER_DECIMAL_POINT = 22,
    NUMBER_DIGIT = 23
}
type ParserEvent = (parser: ClarinetParser, event: string, data?: any) => void;
export type ClarinetParserOptions = {
    onready?: ParserEvent;
    onopenobject?: ParserEvent;
    onkey?: ParserEvent;
    oncloseobject?: ParserEvent;
    onopenarray?: ParserEvent;
    onclosearray?: ParserEvent;
    onvalue?: ParserEvent;
    onerror?: ParserEvent;
    onend?: ParserEvent;
    onchunkparsed?: ParserEvent;
};
export default class ClarinetParser {
    protected options: Required<ClarinetParserOptions>;
    bufferCheckPosition: number;
    q: string;
    c: string;
    p: string;
    closed: boolean;
    closedRoot: boolean;
    sawRoot: boolean;
    error: Error | null;
    state: STATE;
    stack: STATE[];
    position: number;
    column: number;
    line: number;
    slashed: boolean;
    unicodeI: number;
    unicodeS: string | null;
    depth: number;
    textNode: any;
    numberNode: any;
    constructor(options?: ClarinetParserOptions);
    end(): this;
    resume(): this;
    close(): void | this;
    emit(event: string, data?: any): void;
    emitNode(event: string, data?: any): void;
    write(chunk: any): void | this;
    _closeValue(event?: string): void;
    _closeNumber(): void;
    _error(message?: string): void;
}
export {};
//# sourceMappingURL=clarinet.d.ts.map