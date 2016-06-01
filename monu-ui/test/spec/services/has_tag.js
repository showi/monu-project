'use strict';

describe('Service: hasTag', function () {

  // load the service's module
  beforeEach(module('monoApp'));

  // instantiate service
  var hasTag;
  beforeEach(inject(function (_hasTag_) {
    hasTag = _hasTag_;
  }));

  it('should do something', function () {
    expect(!!hasTag).toBe(true);
  });

});
