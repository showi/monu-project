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

    Service.get = function (collection, key, tag_list, method) {
      if (tag_list instanceof Array) {
        if (tag_list.length == 0) {
          return null;
        }
        var newlist = [];
        for (var i = 0, item; tag_list.length, item = tag_list[i]; i++) {
          newlist.push(item.name);
        }
        tag_list = newlist.join(',');
      }
      method = method === undefined ? 'GET' : method;
      var url = Util.join(urlPrefix, collection, key, tag_list);
      return $http({
        'method': method,
        'url': url
      });
    };

  }]);
