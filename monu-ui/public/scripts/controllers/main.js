'use strict';

/**
 * @ngdoc function
 * @name monoApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the monoApp
 */
angular.module('monoApp')
  .controller('MainCtrl', ['$route', function ($route) {
    this.$route = $route;
  }]);
