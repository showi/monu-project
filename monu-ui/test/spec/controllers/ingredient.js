'use strict';

describe('Controller: IngredientCtrl', function () {

  // load the controller's module
  beforeEach(module('monoApp'));

  var IngredientCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    IngredientCtrl = $controller('IngredientCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(IngredientCtrl.awesomeThings.length).toBe(3);
  });
});
