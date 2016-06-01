'use strict';

/**
 * @ngdoc function
 * @name monoApp.controller:IngredientCtrl
 * @description
 * # IngredientCtrl
 * Controller of the monoApp
 */
angular.module('monoApp')
  .controller('IngredientCtrl', ['$route', '$scope', 'Ingredient', 'Tag', 'Schema', 'Util', 'HasIngredient',
    function ($route, $scope, Ingredient, Tag, Schema, Util, HasIngredient) {

      var Ctl = this;
      Ctl.data = [];
      Ctl.TagService = Tag;
      Ctl.related = [];
      Ctl.get = function (url) {
        Ingredient.get(url).then(function (response) {
            if (response.status !== 200) {
              console.error('Cannot get ingredient: %s (%s)', response.status_text, response.config.url);
            }
            angular.copy(response.data, Ctl.data);
            if (Ctl.data.length == 1) {
              for (var i = 0, doc; i < Ctl.data.length, doc = Ctl.data[i]; i++) {
                console.log('Response', doc);
                if (!Util.isEmpty(doc.name)) {
                  HasIngredient.get('recipe', doc.name).then(function (tag_list) {
                    console.log('Taglist', tag_list);
                    for (var i = 0, tag; i < tag_list.data.length, tag = tag_list.data[i]; i++) {
                      console.log('Pushing ingredient: %s', tag);
                      Ctl.related.push(tag);
                    }
                  });
                }
              }
            }
          }
        );
      };

      Ctl._init = function () {
        var op = $route.current.$$route.originalPath;
        if (0 === op.indexOf('/ingredient/edit/:key/:value')) {
          Ctl.Schema = Schema.get('/ingredient');
          Ctl.StartVal = Ingredient.get(Util.join($route.current.params.key, $route.current.params.value)).then(function (response) {
            return response.data;
          });
        } else if (0 === op.indexOf('/ingredient/view/:key/:value')) {
          Ctl.get(Util.join($route.current.params.key, $route.current.params.value));
        } else {
          Ctl.get();
        }
      };

      Ctl._init();
    }])
;
