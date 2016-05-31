'use strict';

/**
 * @ngdoc function
 * @name monoApp.controller:RecipeCtrl
 * @description
 * # RecipeCtrl
 * Controller of the monoApp
 */
angular.module('monoApp')
  .controller('RecipeCtrl', ['$route', '$scope', 'Recipe', 'Ingredient', 'Tag', 'Schema', 'Util',
    function ($route, $scope, Recipe, Ingredient, Tag, Schema, Util) {

      var Ctl = this;

      Ctl.data = [];
      Ctl.TagService = Tag;

      Ctl.get = function (url) {
        Recipe.get(url).then(function (response) {
          if (response.status !== 200) {
            console.error('Cannot get recipe: %s (%s)', response.status_text, response.config.url);
          }
          angular.copy(Recipe.restructure(response.data), Ctl.data);
        });
      };

      Ctl._init = function () {
        var op = $route.current.$$route.originalPath;
        if (0 === op.indexOf('/recipe/edit/:key/:value')) {
          Ctl.Schema = Schema.get('/recipe');
          Ctl.StartVal = Recipe.get(Util.join($route.current.params.key, $route.current.params.value)).then(function (response) {
            return response.data;
          });
        } else if (0 === op.indexOf('/recipe/view/:key/:value')) {
          Ctl.get(Util.join($route.current.params.key, $route.current.params.value));
        } else {
          Ctl.get();
        }
      };

      Ctl._init();

    }]);
