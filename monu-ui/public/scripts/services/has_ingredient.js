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

    Service.get = function (collection, ingredient_list, method) {
      method = method === undefined ? 'GET' : method;
      var url = Util.join(urlPrefix, collection, ingredient_list);
      return $http({
        'method': method,
        'url': url
      });
    };
  }]);
