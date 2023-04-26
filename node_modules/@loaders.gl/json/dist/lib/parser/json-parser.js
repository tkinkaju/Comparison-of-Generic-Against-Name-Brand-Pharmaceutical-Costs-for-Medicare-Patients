"use strict";
// @ts-nocheck
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const clarinet_1 = __importDefault(require("../clarinet/clarinet"));
const jsonpath_1 = __importDefault(require("../jsonpath/jsonpath"));
// JSONParser builds a JSON object using the events emitted by the Clarinet parser
class JSONParser {
    constructor(options) {
        this.result = undefined;
        this.previousStates = [];
        this.currentState = Object.freeze({ container: [], key: null });
        this.jsonpath = new jsonpath_1.default();
        this.reset();
        this.parser = new clarinet_1.default({
            onready: () => {
                this.jsonpath = new jsonpath_1.default();
                this.previousStates.length = 0;
                this.currentState.container.length = 0;
            },
            onopenobject: (name) => {
                this._openObject({});
                if (typeof name !== 'undefined') {
                    this.parser.emit('onkey', name);
                }
            },
            onkey: (name) => {
                this.jsonpath.set(name);
                this.currentState.key = name;
            },
            oncloseobject: () => {
                this._closeObject();
            },
            onopenarray: () => {
                this._openArray();
            },
            onclosearray: () => {
                this._closeArray();
            },
            onvalue: (value) => {
                this._pushOrSet(value);
            },
            onerror: (error) => {
                throw error;
            },
            onend: () => {
                this.result = this.currentState.container.pop();
            },
            ...options
        });
    }
    reset() {
        this.result = undefined;
        this.previousStates = [];
        this.currentState = Object.freeze({ container: [], key: null });
        this.jsonpath = new jsonpath_1.default();
    }
    write(chunk) {
        this.parser.write(chunk);
    }
    close() {
        this.parser.close();
    }
    // PRIVATE METHODS
    _pushOrSet(value) {
        const { container, key } = this.currentState;
        if (key !== null) {
            container[key] = value;
            this.currentState.key = null;
        }
        else {
            container.push(value);
        }
    }
    _openArray(newContainer = []) {
        this.jsonpath.push(null);
        this._pushOrSet(newContainer);
        this.previousStates.push(this.currentState);
        this.currentState = { container: newContainer, isArray: true, key: null };
    }
    _closeArray() {
        this.jsonpath.pop();
        this.currentState = this.previousStates.pop();
    }
    _openObject(newContainer = {}) {
        this.jsonpath.push(null);
        this._pushOrSet(newContainer);
        this.previousStates.push(this.currentState);
        this.currentState = { container: newContainer, isArray: false, key: null };
    }
    _closeObject() {
        this.jsonpath.pop();
        this.currentState = this.previousStates.pop();
    }
}
exports.default = JSONParser;
