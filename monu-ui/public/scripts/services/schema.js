'use strict';

/**
 * @ngdoc service
 * @name monoApp.schema
 * @description
 * # schema
 * Service in the monoApp.
 */
angular.module('monoApp')
.service('Schema', ['$http', 'Util', function ($http, Util) {

  var Service = this;
  var urlPrefix = '/api/schema';

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
  }]);
