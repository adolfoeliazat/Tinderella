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
    $scope.cardsLiked = [];

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
        mixpanel.track("card.dislike");
        console.log('Card disliked is ' + $scope.cards[index].id);
    };

    $scope.cardSwipedRight = function(index) {
        var cardLiked = $scope.cards[index];

        if ($scope.cardsLiked.indexOf(cardLiked.id) === -1) {
            $scope.cardsLiked.push(cardLiked.id);
        }

        mixpanel.track("card.like");
        console.log('Card liked is ' + cardLiked.id);
    };

    $scope.cardDestroyed = function(index) {
        $scope.cards.splice(index, 1);

        // After the user goes through all the images, display the results from the backend
        if ($scope.cards.length === 0) {
            if ($scope.cardsLiked.length === 0) {
                window.open('/', '_self');
            }
            else {
                $('#loader_section').show();
                $('.like_dislike_buttons').css('display', 'none');

                console.log('Processing results...');
                mixpanel.track("results.view");
                $.ajax({
                    url: '/results',
                    type: 'POST',
                    dataType: 'html',
                    data: { cards_liked: JSON.stringify($scope.cardsLiked) },
                    success: function(html) {
                        // Navigate to the results page once done
                        var newDoc = document.open('text/html', 'replace');
                        newDoc.write(html);
                        newDoc.close();
                    }
                });
            }
        }
    };
});
