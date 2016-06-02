'use strict';

/**
 * @ngdoc service
 * @name monoApp.hasIngredient
 * @description
 * # hasIngredient
 * Service in the monoApp.
 */
angular.module('monoApp')
  .service('HasIngredient', ['$http', 'Util', function ($http, Util) {
    var Service = this;
    var urlPrefix = '/api/has/ingredient';

    Service.get = function (collection, key, ingredient_list, method) {
      console.log('HasIngredient', collection, key, ingredient_list, method);
      if (ingredient_list instanceof Array) {
        if (ingredient_list.length == 0) {
          return null;
        }
        var newlist = [];
        for(var i = 0, item; ingredient_list.length, item=ingredient_list[i]; i++) {
          newlist.push(item.name);
        }
        ingredient_list = newlist.join(',');
      }
      method = method === undefined ? 'GET' : method;
      var url = Util.join(urlPrefix, collection, key, ingredient_list);
      return $http({
        'method': method,
        'url': url
      });
    };
  }]);
