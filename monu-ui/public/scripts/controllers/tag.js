'use strict';

/**
 * @ngdoc function
 * @name monoApp.controller:TagCtrl
 * @description
 * # TagCtrl
 * Controller of the monoApp
 */
angular.module('monoApp')
  .controller('TagCtrl', ['$route', '$scope', 'Tag', 'Schema', 'Util', 'HasTag',
    function ($route, $scope, Tag, Schema, Util, HasTag) {

      var Ctl = this;
      Ctl.data = [];
      Ctl.related = [];
      /* Populate controller with tag data
       */
      Ctl.get = function (url) {
        Tag.get(url).then(function (response) {
          if (response.status !== 200) {
            console.error('Cannot get tag: %s (%s)', response.status_text, response.config.url);
          } else {
            angular.copy(response.data, Ctl.data);
            if (Ctl.data.length == 1) {
              for (var i = 0, doc; i < Ctl.data.length, doc = Ctl.data[i]; i++) {
                if (!Util.isEmpty(doc._id)) {
                  HasTag.get('recipe', '_id', doc._id).then(function (tag_list) {
                    for (var i = 0, tag; i < tag_list.data.length, tag = tag_list.data[i]; i++) {
                      Ctl.related.push(tag);
                    }
                  });
                }
              }
            }
          }
        });
      };

      /* Initialize our controller
       */
      Ctl._init = function () {
        var op = $route.current.$$route.originalPath;
        if (0 === op.indexOf('/tag/edit/:key/:value')) {
          Ctl.Schema = Schema.get('/tag');
          Ctl.StartVal = Tag.get(Util.join($route.current.params.key, $route.current.params.value)).then(function (response) {
            return response.data;
          });
        } else if (0 === op.indexOf('/tag/view/:key/:value')) {
          Ctl.get(Util.join($route.current.params.key, $route.current.params.value));
        } else {
          Ctl.get();
        }
      };

      /* Main
       */
      Ctl._init();
    }]);
