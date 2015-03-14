// Ionic Starter App, v0.9.20

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'ionic.contrib.ui.tinderCards' is found in ionic.tdcards.js
angular.module('starter', ['ionic', 'ionic.contrib.ui.tinderCards'])

.directive('noScroll', function() {
    return {
        restrict: 'A',
        link: function($scope, $element, $attr) {
            $element.on('touchmove', function(e) {
                e.preventDefault();
            });
        }
    }
})

.controller('CardsCtrl', function($scope) {
    // var walk = require('walk');
    var cardTypes = [
        { image: 'img/nordstrom_832471.jpg'},
        { image: 'img/barneys_503643730.jpg'},
        { image: 'img/barneys_503643746.jpg'},
        { image: 'img/saks_0469642478019.jpg'},
    ];

    $scope.cards = [];

    $scope.addCard = function(i) {
        var randInd = Math.floor(Math.random() * cardTypes.length);
        var newCard = cardTypes[randInd];
        newCard.id = Math.random();
        $scope.cards.push(angular.extend({}, newCard));
        cardTypes.splice(randInd, 1);
    }


    for(var i = 0; i < 4; i++) $scope.addCard();

    $scope.cardSwipedLeft = function(index) {
        console.log('Left swipe');
    }

    $scope.cardSwipedRight = function(index) {
        console.log('Right swipe');
    }

    $scope.cardDestroyed = function(index) {
        $scope.cards.splice(index, 1);
        console.log('Card removed');
    }
});
