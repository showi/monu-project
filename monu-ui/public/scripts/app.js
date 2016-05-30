'use strict';

/**
 * @ngdoc overview
 * @name monoApp
 * @description
 * # monoApp
 *
 * Main module of the application.
 */
angular
  .module('monoApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'schemaForm',
    'angular-json-editor'
])
  .config(function ($routeProvider, JSONEditorProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/recipe.html',
        controller: 'RecipeCtrl',
        controllerAs: 'recipe'
      })
      .when('/recipe/view', {
        templateUrl: 'views/recipe.html',
        controller: 'RecipeCtrl',
        controllerAs: 'recipe'
      })
      .when('/recipe/view/:key/:value', {
        templateUrl: 'views/recipe-view.html',
        controller: 'RecipeCtrl',
        controllerAs: 'recipe'
      })
      .when('/recipe/edit/:key/:value', {
        templateUrl: 'views/recipe-edit.html',
        controller: 'RecipeCtrl',
        controllerAs: 'recipe'
      })
      .when('/tag/view', {
        templateUrl: 'views/tag.html',
        controller: 'TagCtrl',
        controllerAs: 'tag'
      })
      .when('/tag/view/:key/:value', {
        templateUrl: 'views/tag-view.html',
        controller: 'TagCtrl',
        controllerAs: 'tag'
      })
      .when('/tag/edit/:key/:value', {
        templateUrl: 'views/tag-edit.html',
        controller: 'TagCtrl',
        controllerAs: 'tag'
      })
      .when('/ingredient/view', {
        templateUrl: 'views/ingredient.html',
        controller: 'IngredientCtrl',
        controllerAs: 'ingredient'
      })
      .when('/ingredient/view/:key/:value', {
        templateUrl: 'views/ingredient-view.html',
        controller: 'IngredientCtrl',
        controllerAs: 'ingredient'
      })
      .when('/ingredient/edit/:key/:value', {
        templateUrl: 'views/ingredient-edit.html',
        controller: 'IngredientCtrl',
        controllerAs: 'ingredient'
      })
      .otherwise({
        redirectTo: '/'
      });

      JSONEditorProvider.configure({
            plugins: {
                sceditor: {
                    style: 'sce/development/jquery.sceditor.default.css'
                }
            },
            defaults: {
                options: {
                    iconlib: 'bootstrap3',
                    theme: 'bootstrap3',
                    ajax: true
                }
            }
        });
  });
