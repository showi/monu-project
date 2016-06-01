'use strict';

/**
 * @ngdoc service
 * @name monoApp.hasTag
 * @description
 * # hasTag
 * Service in the monoApp.
 */
angular.module('monoApp')
  .service('HasTag', ['$http', 'Util', function ($http, Util) {

    var Service = this;
    var urlPrefix = '/api/has/tag';

    Service.get = function (collection, tag_list, method) {
      method = method === undefined ? 'GET' : method;
      var url = Util.join(urlPrefix, collection, tag_list);

      return $http({
        'method': method,
        'url': url
      });
    };

  }]);
