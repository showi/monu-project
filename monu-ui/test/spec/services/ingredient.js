'use strict';

describe('Service: ingredient', function () {

  // load the service's module
  beforeEach(module('monoApp'));

  // instantiate service
  var ingredient;
  beforeEach(inject(function (_ingredient_) {
    ingredient = _ingredient_;
  }));

  it('should do something', function () {
    expect(!!ingredient).toBe(true);
  });

});
