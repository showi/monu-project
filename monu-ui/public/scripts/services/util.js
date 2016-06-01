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
      isEmpty: function(obj) {
        if (obj === undefined) {
          return true;
        }
        console.log('Typeof object', typeof obj)
        if (typeof obj === 'string') {
          if(obj == '') {
            return true;
          }
          return false;
        } else {
          throw 'Using isEmpty on unsupported data type';
        }
      },
      join: function() {
        return [].join.call(arguments, '/');
      }
    };
  });
