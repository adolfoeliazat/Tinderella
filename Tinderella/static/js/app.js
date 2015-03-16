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
    $scope.cards = [];
    $scope.cardsArchive = [];

    $.ajax({
        url: '/images',
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            var urls = data['images'];
            if(!$scope.allCards) {
                $scope.allCards = [];
                urls.map(function(url, index) {
                    $scope.allCards.push({id: index, url: '/static/shoes/' + url });
                });
            }

            $scope.addCard = function(i) {
                var randInd = Math.floor(Math.random() * $scope.allCards.length);
                var newCard = $scope.allCards[randInd];

                $scope.cards.push(newCard);
                $scope.allCards.splice(randInd, 1);
            };

            for(var i = 0; i < 5; i++) {
                $scope.addCard();
            }

            $scope.cardsArchive = $scope.cards.slice();
        },
           
        error: function(err) {
          console.log(err);
        },

        // NOTE: Ensures that $scope.cards is populated before ionic renders the tinder-like cards
        async: false
    });

    $scope.cardSwipedLeft = function(index) {
        console.log('Card disliked is ' + $scope.cards[index].id);
    };

    $scope.cardSwipedRight = function(index) {
        var cardLiked = $scope.cards[index];
        console.log('Card liked is ' + cardLiked.id);

        // Send the like back to the backend
        $.ajax({
            url: '/cards/' + cardLiked.id + '/like',
            type: 'POST',
            dataType: 'json'
        });
    };

    $scope.cardDestroyed = function(index) {
        $scope.cards.splice(index, 1);

        // After the user goes through all the images, display the results from the backend
        if ($scope.cards.length === 0) {
            $('#loader_section').show();
            $('.like_dislike_buttons').css('display', 'none');

            console.log('Processing results...');
            $.ajax({
                url: '/process_results',
                type: 'POST',
                dataType: 'json',
                success: function(return_code) {
                    if (return_code.success) {
                        // Navigate to the results page once done
                        window.open('/results', '_self');
                    } else {
                        window.open('/', '_self');
                    }
                }
            });
        }
    };
});
