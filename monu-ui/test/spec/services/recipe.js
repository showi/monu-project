'use strict';

describe('Service: recipe', function () {

  // load the service's module
  beforeEach(module('monoApp'));

  // instantiate service
  var recipe;
  beforeEach(inject(function (_recipe_) {
    recipe = _recipe_;
  }));

  it('should do something', function () {
    expect(!!recipe).toBe(true);
  });

});
