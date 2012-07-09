/**
 * Provides an enhanced user interface.
 */

$(document).ready(function() {
	
	// Show javascript only elements.
	enableJavascriptOnlyElements();

	// Transform the active elements.
	transformActiveElements();

	// Add the event actions.
	setupConditionallyVisibleElements();

	// Transform the wizards.
	transformWizards();
});

/**
 * \brief Removes the display: hidden attribute from "javascript-only"
 * elements.
 */
function enableJavascriptOnlyElements() {
	$('.javascript-only').removeClass('javascript-only');
}

/**
 * \brief Transform active elements.
 */
function transformActiveElements() {

	// The list filters.
	$('input.list-filter[type="text"]').bind('input', updateListFilter);
	$('input.list-filter[type="text"]').updateListFilter();
	
	// Hide the list filter defaults
	$('.list-filter-default').hide();

	// Transform the certificate textareas
	$('textarea[data-content-type="application/x-x509-ca-cert"]').fileTextarea();
	$('textarea[data-content-type="application/x-pem-key"]').fileTextarea();
}

/**
 * \brief Setup visibility actions.
 */
function setupConditionallyVisibleElements() {
	// Transform the conditionally visible elements.
	$('.conditionally-visible').conditionallyVisible();
}

/**
 * \brief Transform wizards.
 */
function transformWizards() {
	$('.wizard').wizard();
}

/* The components functions */

function updateListFilter() {

	$(this).each(function () {
		var associated_list = $(this).attr('data-associated-list');

		if (associated_list && associated_list.length) {

			var filter_attribute = $(this).attr('data-filter-attribute');
			var filter_text = $(this).val();
			var default_text = $('.list-filter-default[data-associated-list="' + associated_list + '"]');

			var items = $('ul[data-list-name="' + associated_list + '"] li');
			var filtered_items = items.filter(function () { return ($(this).attr(filter_attribute).indexOf(filter_text) > -1); });

			if (filtered_items.length) {
				default_text.hide();

				var filtered_out_items = items.filter(function () { return ($(this).attr(filter_attribute).indexOf(filter_text) == -1); });

				filtered_items.show(100);
				filtered_out_items.hide(100);
			} else {
				default_text.show(100);
				items.hide(100);
			}
		}
	});
}

function fileTextarea() {

	$(this).each(function () {
		if (FileReader) {

			var textarea = $(this);
			var input = $(document.createElement('input'));
			input.attr('type', 'file');

			input.change(function (evt) {
				var file = evt.target.files[0];

				if (file) {

					var reader = new FileReader();

					reader.onload = function(evt) {
						textarea.text(evt.target.result);
					}

					reader.readAsText(file);
				}
			});

			textarea.before(input);
			textarea.change(function() {
				input.val('');
			});
		}
	});
}

function conditionallyVisible() {

	$(this).each(function () {

		var element = $(this);
		var target = $(document.getElementById(element.attr('data-conditional-visibility-target')));

		$('input[name="' + target.attr('name') + '"]').bind('change', function () {
			if (target.is(':checked')) {
				element.show(100);
			} else {
				element.hide(100);
			}
		});

		if (!target.is(':checked')) {
			element.hide();
		}
	});
}

function wizard() {

	$(this).each(function () {

		var form = $(this)
		var fieldsets = $(this).children('fieldset:not(.wizard-buttons-fieldset)');
		var cancel_button = $(this).find('.wizard-button-cancel');
		var previous_button = $(this).find('.wizard-button-previous');
		var next_button = $(this).find('.wizard-button-next');
		var submit_button = $(this).find('.wizard-button-submit');

		// Set the current page.
		var page_count = fieldsets.length;
		
		// The function to rule them all.
		form.setPage = function (page, delay) {

			form.attr('data-current-page', page);

			if (page < 0) {
				page = 0;
			} else if (page >= page_count) {
				page = page_count - 1;
			}

			if (page == 0) {
				previous_button.addClass('disabled');
			} else {
				previous_button.removeClass('disabled');
			}

			if (page == page_count - 1) {
				next_button.addClass('disabled');
				next_button.hide();
				submit_button.removeAttr('disabled');
				submit_button.show();
			} else {
				next_button.removeClass('disabled');
				next_button.show();
				submit_button.attr('disabled', 'disabled');
				submit_button.hide();
			}

			for (i = 0; i < page_count; ++i) {
				if (i == page) {
					$(fieldsets[i]).show(delay);
				} else {
					$(fieldsets[i]).hide(delay);
				}
			}
		}

		// Set the buttons actions.
		next_button.click(function () {

			if (!$(this).is('.disabled')) {
				form.setPage((form.attr('data-current-page') || 0) + 1, 200);
			}

			return false;
		});

		previous_button.click(function () {

			if (!$(this).is('.disabled')) {
				form.setPage((form.attr('data-current-page') || 0) - 1, 200);
			}

			return false;
		});

		// Hide all the fieldsets except the first one.
		form.setPage(0);
	});
}

/* Extend JQuery */

jQuery.fn.extend({
	updateListFilter: updateListFilter,
	fileTextarea: fileTextarea,
  conditionallyVisible: conditionallyVisible,
  wizard: wizard
});
