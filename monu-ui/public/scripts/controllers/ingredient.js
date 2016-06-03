'use strict';

/**
 * @ngdoc function
 * @name monoApp.controller:IngredientCtrl
 * @description
 * # IngredientCtrl
 * Controller of the monoApp
 */
angular.module('monoApp')
  .controller('IngredientCtrl', ['$route', '$scope', 'Ingredient', 'Tag', 'Schema', 'Util', 'HasIngredient', 'HasTag',
    function ($route, $scope, Ingredient, Tag, Schema, Util, HasIngredient, HasTag) {

      var Ctl = this;
      Ctl.data = [];
      Ctl.TagService = Tag;
      Ctl.related = [];
      Ctl.related_tag = [];
      Ctl.get = function (url) {
        Ingredient.get(url).then(function (response) {
            if (response.status !== 200) {
              console.error('Cannot get ingredient: %s (%s)', response.status_text, response.config.url);
            }
            angular.copy(response.data, Ctl.data);
            if (Ctl.data[0].tag !== undefined && Ctl.data[0].length > 0) {
              var tag_list = '';
              for (var i = 0, c; i < Ctl.data[0].tag.length, c = Ctl.data[0].tag[i]; i++) {
                tag_list += c.name + ',';
              }
              HasTag.get('ingredient', '_id', tag_list).then(function (response) {
                angular.copy(response.data, Ctl.related_tag);
              });
            }
            if (Ctl.data.length == 1) {
              for (var i = 0, doc; i < Ctl.data.length, doc = Ctl.data[i]; i++) {
                if (!Util.isEmpty(doc._id)) {
                  HasIngredient.get('recipe', '_id', doc._id).then(function (response) {
                    for (var i = 0, tag; i < response.data.length, tag = response.data[i]; i++) {
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
