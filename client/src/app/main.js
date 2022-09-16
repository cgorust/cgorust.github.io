import {Word} from './word.js';
import {Config} from './config.js';
import {Converter} from './converter.js';

class Main {
  constructor() {
    new Word();
    new Config(config => {});
    new Converter();
  }
}

$(document).ready(function() {
  new Main();
})