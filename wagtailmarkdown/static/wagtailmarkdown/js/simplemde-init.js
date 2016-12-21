"use strict";

function initSimpleMDE(id, options) {
  options.element = document.getElementById(id);
  return new SimpleMDE(options);
}
