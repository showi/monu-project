'use strict';

describe('Service: schema', function () {

  // load the service's module
  beforeEach(module('monoApp'));

  // instantiate service
  var schema;
  beforeEach(inject(function (_schema_) {
    schema = _schema_;
  }));

  it('should do something', function () {
    expect(!!schema).toBe(true);
  });

});
