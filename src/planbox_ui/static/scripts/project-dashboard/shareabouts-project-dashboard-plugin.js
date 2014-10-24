/*globals Backbone, jQuery, Modernizr, Handlebars */

var Planbox = Planbox || {};

(function(NS, $) {
  'use strict';

  // Exceptions ===============================================================
  NS.shareaboutsException = function(message, data) {
    return NS.genericException('ShareaboutsException', message, data);
  };

  // App ======================================================================
  // (NS.app is defined in base-app.js)

  var syncWithCredentials = function(method, model, options) {
    _.defaults(options || (options = {}), {
      xhrFields: {withCredentials: true}
    });

    return Backbone.sync.apply(this, [method, model, options]);
  };

  NS.ShareaboutsDashboardPlugin = NS.Plugin.extend({
    initialize: function() {
      this.config = this.getShareaboutsConfig();
      this.dataset = new Backbone.Model();
      this.dataset.url = this.config.details.dataset_url;
      this.dataset.sync = syncWithCredentials;
      this.dataset.fetch();

      this.app.on('show:projectDashboard:activityPanel:after', _.bind(this.onShowActivityPanel, this));
    },

    getShareaboutsConfig: function() {
      var projectSections = NS.Data.project.sections,
          shareaboutsSection = _.findWhere(projectSections, {type: 'shareabouts'});
      return shareaboutsSection;
    },

    onShowActivityPanel: function() {

    }
  });

}(Planbox, jQuery));