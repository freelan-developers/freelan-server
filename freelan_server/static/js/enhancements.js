/**
 * Provides an enhanced user interface.
 */

$(document).ready(function() {

	// Show javascript only elements.
	$('.javascript-only').removeClass('javascript-only');

	// Transform the active elements.
	transformActiveElements();

	// Add the event actions.
	$('.conditionally-visible').conditionallyVisible();

	// Transform the wizards.
	$('.wizard').wizard();

	// Transform the multiple selects into tag lists.
	$('select[multiple]').tagList();
});

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

/* The components functions */

function updateListFilter() {

	$(this).each(function () {
		var associated_list = $(this).attr('data-associated-list');

		if (associated_list && associated_list.length) {

			var filter_attribute = $(this).attr('data-filter-attribute');
			var filter_text = $(this).val().toUpperCase();
			var default_text = $('.list-filter-default[data-associated-list="' + associated_list + '"]');

			var items = $('ul[data-list-name="' + associated_list + '"] li');
			var filtered_items = items.filter(function () { return ($(this).attr(filter_attribute).toUpperCase().indexOf(filter_text) > -1); });

			if (filtered_items.length) {
				default_text.hide();

				var filtered_out_items = items.filter(function () { return ($(this).attr(filter_attribute).toUpperCase().indexOf(filter_text) == -1); });

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

		var form = $(this);
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

function tagList() {

	$(this).each(function () {
		var select = $(this);
		var options = select.children('option');
		var disable_blur = false;
		var selection_index = 0;

		var tag_list = $(document.createElement('div'));
		tag_list.attr('class', select.attr('class'));
		tag_list.addClass('tag-list');
		select.after(tag_list);

		if (select.attr('disabled')) {
			tag_list.attr('disabled', '');
		}

		var ul = $(document.createElement('ul'));
		ul.addClass('tags');
		tag_list.append(ul);

		var input_li = $(document.createElement('li'));
		input_li.addClass('input');
		ul.append(input_li);

		var input = $(document.createElement('input'));
		input.attr('type', 'text');
		input_li.append(input);

		var suggestions = $(document.createElement('ul'));
		suggestions.addClass('suggestions');
		tag_list.append(suggestions);

		var no_result = $(document.createElement('li'));
		no_result.addClass('empty');
		no_result.text('No result');
		suggestions.append(no_result);

		function valueSelected(value) {
			var option = options.filter('[value="' + value + '"]');

			return option.is('[selected]');
		}

		function selectValue(value) {
			var option = options.filter('[value="' + value + '"]');

			option.attr('selected', 'selected');
		}

		function unselectValue(value) {
			var option = options.filter('[value="' + value + '"]');

			option.removeAttr('selected');
		}

		function removeTag(value) {
			var li = ul.children('li.tag[data-value="' + value + '"]');

			li.remove();
		}

		function addTag(value, label) {
			var li = $(document.createElement('li'));
			li.addClass('tag');
			li.attr('data-value', value);
			li.text(label);

			if (!tag_list.attr('disabled')) {
				var a = $(document.createElement('a'));
				a.attr('href', '');
				a.click(function() { removeTag(value); unselectValue(value); return false; });
				li.append(a);
			}

			var last_tag = ul.children('li.tag:last');

			if (last_tag.length) {
				li.insertAfter(last_tag);
			} else {
				ul.prepend(li);
			}
		}

		function updateFilter() {

			var top = tag_list.position().top + tag_list.outerHeight();
			var left = input.position().left;

			suggestions.css({ top: top + "px", left: left + "px" });

			var filter_text = input.val().toUpperCase();
			var items = suggestions.children('li.value');
			var unselected_items = items.filter(function () { return !valueSelected($(this).attr('data-value')); });
			var filtered_items = unselected_items.filter(function () { return ($(this).attr('data-label').toUpperCase().indexOf(filter_text) > -1); });

			items.hide();
			items.removeClass('selection');

			if (filtered_items.length) {
				no_result.hide();
				filtered_items.show();

				var index = (selection_index >= filtered_items.length) ? filtered_items.length - 1 : selection_index;

				$(filtered_items[index]).addClass('selection');
				input.removeClass('empty');
			} else {
				no_result.show();
				input.addClass('empty');
			}
		}

		if (tag_list.attr('disabled')) {
			input.attr('disabled', '');
		} else {
			// Convenience: clicking on the tag_list focuses the input.
			tag_list.click(function() { input.focus(); });

			// Convenience: focusing or bluring the input, apply/disable a style on the
			// tag_list.
			input.focus(function() { tag_list.addClass('focused'); updateFilter(); suggestions.show(); });
			input.blur(function(evt) { tag_list.removeClass('focused'); if (!disable_blur) { suggestions.hide(); input.val(''); } });
		}

		input.bind('input', function(evt) {
			updateFilter();
		});

		input.keydown(function(evt) {
			if (evt.which == 13) { // Return
				evt.preventDefault();

				var items = suggestions.children('li.value.selection');

				if (items.length) {
					var value = $(items[0]).attr('data-value');
					var text = $(items[0]).attr('data-label');
					selectValue(value);
					addTag(value, text);
					input.val('');
					selection_index = 0;

					updateFilter();
				}
			} else if (evt.which == 8) { // Backspace

				// If the input is empty, remove the last tag.
				if (input.val() == '') {
					evt.preventDefault();

					var last_tag = ul.children('li.tag:last');

					if (last_tag) {
						var value = last_tag.attr('data-value');
						unselectValue(value);
						last_tag.remove();
					}
				}

				updateFilter();
			} else if (evt.which == 38) { // Up
				selection_index = (selection_index > 0) ? selection_index - 1 : 0;
				updateFilter();
			} else if (evt.which == 40) { // Down
				var filtered_items_count = suggestions.children('li.value').filter(':visible').length;
				selection_index = (selection_index < filtered_items_count - 1) ? selection_index + 1 : filtered_items_count - 1;
				updateFilter();
			}
		});

		suggestions.mouseenter(function () {
			disable_blur = true;
		});

		suggestions.mouseleave(function () {
			disable_blur = false;

			if (!input.is(':focus')) {
				suggestions.hide();
				input.val('');
			}
		});

		// Populates the suggestions
		options.each(function() {
			var option = $(this);
			var item = $(document.createElement('li'));
			item.addClass('value');
			item.attr('data-value', option.val());
			item.attr('data-label', option.text());
			item.text(option.text());

			item.click(function() {
				selectValue(option.val());
				addTag(option.val(), option.text());
				input.val('');
			});

			var last_item = suggestions.children('li.value:last');

			if (last_item.length) {
				item.insertAfter(last_item);
			} else {
				suggestions.prepend(item);
			}
		});

		// Populates the list with the selected options
		options.filter(':selected').each(function () {
			var option = $(this);
			addTag(option.val(), option.text());
		});

		suggestions.hide();
		select.hide();
	});
}

/* Extend JQuery */

jQuery.fn.extend({
	updateListFilter: updateListFilter,
	fileTextarea: fileTextarea,
	conditionallyVisible: conditionallyVisible,
	wizard: wizard,
	tagList: tagList,
});
