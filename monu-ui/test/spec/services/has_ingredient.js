'use strict';

describe('Service: hasIngredient', function () {

  // load the service's module
  beforeEach(module('monoApp'));

  // instantiate service
  var hasIngredient;
  beforeEach(inject(function (_hasIngredient_) {
    hasIngredient = _hasIngredient_;
  }));

  it('should do something', function () {
    expect(!!hasIngredient).toBe(true);
  });

});
