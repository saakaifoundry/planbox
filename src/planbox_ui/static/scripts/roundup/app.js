/*globals Backbone, jQuery, Modernizr, Handlebars */

var Planbox = Planbox || {};

(function(NS, $) {
  'use strict';

  // Exceptions ===============================================================
  NS.roundupException = function(message, data) {
    return NS.genericException('RoundupException', message, data);
  };

  // App ======================================================================
  // (NS.app is defined in base-app.js)

  NS.app.addInitializer(function(options){
    // Construct models from bootstrapped data
    NS.app.roundupModel = new NS.RoundupModel(NS.Data.profile);

    // Show the main app view
    NS.app.mainRegion.show(new NS.RoundupDisplayView({
      model: NS.app.roundupModel
    }));
  });

}(Planbox, jQuery));