'use strict';

/**
 * @ngdoc service
 * @name monoApp.util
 * @description
 * # util
 * Service in the monoApp.
 */
angular.module('monoApp')
  .service('Util', function () {
    return {
      join: function() {
        return [].join.call(arguments, '/');
      }
    };
  });
