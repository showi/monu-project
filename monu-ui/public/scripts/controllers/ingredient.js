'use strict';

/**
 * @ngdoc function
 * @name monoApp.controller:IngredientCtrl
 * @description
 * # IngredientCtrl
 * Controller of the monoApp
 */
angular.module('monoApp')
  .controller('IngredientCtrl', ['$route', '$scope', 'Ingredient', 'Tag', 'Schema', function ($route, $scope, Ingredient, Tag, Schema) {

    var Ctl = this;
    Ctl.data = [];
    Ctl.TagService = Tag;

    Ctl.get = function(url) {
      Ingredient.get(url).then(function(response) {
        console.log(response);
        if (response.status !== 200) {
          console.error('Cannot get ingredient: %s (%s)', response.status_text, response.config.url);
        }
        angular.copy(response.data, Ctl.data);
      });
    };

    if ($route.current.params.key !== undefined) {
      Ctl.Schema = Schema.get('/ingredient');
      Ctl.StartVal = Ingredient.get('/' + $route.current.params.key + '/' + $route.current.params.value + '?noHeader=1');
    } else {
        Ctl.get();
    }
  }]);
