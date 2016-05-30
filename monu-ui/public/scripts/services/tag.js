'use strict';

/**
 * @ngdoc service
 * @name monoApp.tag
 * @description
 * # tag
 * Service in the monoApp.
 */
angular.module('monoApp')
  .service('Tag', ['$http', 'Util', function ($http, Util) {

    var Service = this;
    var urlPrefix = '/api/tag';

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
