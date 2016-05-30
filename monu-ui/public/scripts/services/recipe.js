'use strict';

/**
 * @ngdoc service
 * @name monoApp.recipe
 * @description
 * # recipe
 * Service in the monoApp.
 */
angular.module('monoApp')
  .service('Recipe', ['$http', 'Util', function ($http, Util) {

    var Service = this;
    var urlPrefix = '/api/recipe';

    Service.get = function (url, method) {
      method = method === undefined ? 'GET' : method;
      if (url !== undefined) {
        url = Util.join(urlPrefix, url);
      } else {
        url = urlPrefix;
      }
      return $http({
        'method': method,
        'url': url
      });
    };

    Service.restructure = function (json) {
      console.log('json', json, typeof json);
      if (!Array.isArray(json)) json = [json];
      console.log('Restructure json: ', json);
      for(var i=0, recipe; i < json.length, recipe=json[i]; i++) {
        if(recipe.child !== undefined && Array.isArray(recipe.child) ) {
          recipe.child_recipe = [];
          console.log('Found child');
          for(var i=0, child; i < recipe.child, child=recipe.child[i]; i++) {
            console.log('Child', child);
            recipe.child_recipe.push(child);
          }
        }
      }

      return json;
    }

  }]);
