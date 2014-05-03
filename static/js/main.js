var application = {
    hostAddForm: {
        init: function() {
            var iName = $('#inputName');
            var iNameControl = $('#nameControlGroup');
            var iDomain = $('#inputDomain');
            var iDomainControl = $('#domainControlGroup');
            var bSubmit = $('.create-hite-form .submit');
            var progressBar = $('.after-create-form-submit');

            createForm = $('#site-create-form');
            createForm.submit(function(){
                createForm.find('.error').removeClass('error');
                createForm.find('.help-inline').remove();
                $('.backend-error').remove();
                helpSpan = $('<span></span>').addClass('help-inline');

                inputName = createForm.find('input[name|="name"]'); 
                // Validate form fields
                inputName.val($.trim(inputName.val()));

                if (!inputName.val() || inputName.val().length < 3) {
                    inputName.focus();
                    if (!inputName.val()) {
                        helpSpan.text(' Введите название сайта');
                    } else {
                        helpSpan.text(' Слишком короткое название сайта');
                    }
                    inputName.parents('.control-group').addClass('error');
                    inputName.after(helpSpan);
                    return false;
                } 
                
                inputDomain = createForm.find('input[name|="domain"]');
                inputDomain.val($.trim(inputDomain.val().toLowerCase()));

                if (!inputDomain.val() || !/^[a-z\d\-\.]{2,}\.[a-z]{2,}$/.test(inputDomain.val())) {
                    inputDomain.focus();
                    if (!inputDomain.val()) {
                        helpSpan.text(' Введите адрес домена');
                    } else {
                        helpSpan.text(' Некорректное имя домена');
                    }
                    inputDomain.parents('.control-group').addClass('error');
                    inputDomain.after(helpSpan);
                    return false;
                }

                requestString = createForm.serialize();

                inputName.attr('disabled', true);
                inputDomain.attr('disabled', true);
                createForm.find('[type|=submit]').addClass('disabled');

                infoDiv = $('<div></div>').addClass('after-create-form');
                progressBar = $('<div></div>').addClass('progress progress-striped active');
                infoText = $('<p></p>').addClass('muted')
                    .text('Подождите, идет создание виртуального хоста');
                progressBar.append($('<div></div>').addClass('bar').css('width', '100%'));
                infoDiv.append(infoText).append(progressBar);
                createForm.after(infoDiv);

                $.ajax({
                    data: requestString,
                    type: "POST",
                    success: function(response) {
                        infoDiv.remove();
                        inputName.attr('disabled', false);
                        inputDomain.attr('disabled', false);
                        createForm.find('[type|=submit]').removeClass('disabled');

                        if (response.success) {
                            /* Insert data into modal window */
                            $('#new-domain').text(inputDomain.val());
                            $('#new-system-user').text(response.data.system.user);
                            $('#new-system-passwd').text(response.data.system.passwd);
                            $('#new-system-host').text(response.data.system.host);
                            $('#new-db-user').text(response.data.db.user);
                            $('#new-db-name').text(response.data.db.user);
                            $('#new-db-passwd').text(response.data.db.passwd);
                            /* Reset form fields */
                            inputName.val('');
                            inputDomain.val('');
                            /* Show modal window */
                            $('#success-modal').modal();
                        } else {
                            errorDiv = $('<div></div>').addClass('backend-error');
                            errorText = $('<p></p>').addClass('alert alert-error');
                            errorDetailLink = $('<a>').attr('href', '#');
                            errorDetailLink.text(' Подробнее');
                            errorText.text('Произошла ошибка.');
                            errorText.append(errorDetailLink);

                            errorDetail = $('<pre></pre>').hide();
                            errorDetailLink.click(function(){
                                if (errorDetail.is(':hidden')) {
                                    errorDetail.show();
                                } else {
                                    errorDetail.hide();
                                }
                                return false;
                            });
                            errorDetailCode = $('<code></code>').text(response.data.err_msg);
                            errorDetail.append(errorDetailCode);

                            errorDiv.append(errorText).append(errorDetail);
                            createForm.after(errorDiv);
                        }
                    },
                });
                return false;
            });
        }
    },
    hostChangeForm: {
        init: function() {
            changeForm = $('#site-change-form');
            changeForm.submit(function(){
                return false;
            });
        }
    },
    hostDeleteForm: {
        init: function() {
            $('.delete-host-form').submit(function(){
                var confirmed = confirm("Подтвердите операцию удаления");
                if (!confirmed) {
                    return false;
                }
                var hostChkDomain = prompt("Внимание! Все данные сайта будут удалены! Введите имя домена для подтверждения.");

                _item = $(this);
                _item.find(".delete-host.btn").addClass("disabled").attr("disabled", true);

                ajaxOptions = {
                    url: _item.attr("action"),
                    type: "POST",
                    data: _item.serialize() + "&domain=" + hostChkDomain
                };
                ajaxOptions.success = function(response) {
                    if (response["success"]) {
                        // Успешное удаление хоста
                        alert("Сайт успешно удален");
                    } else {
                        alert("Произошла ошибка: " + response["data"]["err_msg"])
                    }
                    window.location.reload();
                    return false;
                };

                $.ajax(ajaxOptions);
                return false;
            });
        }
    },
    tabs: {
        init: function() {
            $('#aside-menu-tab a').click(function (e) {
                e.preventDefault();
                $(this).tab('show');
            }); 
        }
    },
    hostList: {
        init: function() {
            $('body').keydown(function (e) {
                var activeItem = $('.site-item.active');
                if (activeItem !== null && activeItem.length) {
                    var siteDetailInfo = $('#site-detail-info');
                    if (siteDetailInfo !== null && siteDetailInfo.length) {
                        console.log(e.keyCode);
                        if (e.keyCode == 13 || e.keyCode == 32) {
                            // Enter or space
                            siteDetailInfo
                                .find('.show-access-data')
                                    .click();
                            return false;
                        } else if (e.keyCode == 46) {
                            // Delete
                            siteDetailInfo
                                .find('.delete-host-form')
                                    .submit();
                            return false;
                        }
                    }
                }
            });
            siteItem = $('.site-item');
            siteItem.click(function() {
                siteItem.removeClass('active');
                siteItem.children('i').each(function(){
                    if (!$(this).parents('li').hasClass('error'))
                        $(this).removeClass('icon-white');
                });

                $(this).addClass('active');
                $(this).children('i').addClass('icon-white');
                url = $(this).attr('href');
                $.ajax({
                    url: url,
                    success: function(msg) {
                        if (msg.success) {
                            host = msg.data;
                            siteDetailInfo = $('#site-detail-info');
                            siteDetailInfo.hide();
                            siteDetailInfo.children('.item-title').text(host.site_name);
                            props = siteDetailInfo.children('.item-properties');
                            props.children('.domain').children('.prop-value').html(
                                $('<a>').attr({
                                    href: 'http://' + host.domain,
                                    target: '_blank'
                                }).text(host.domain));

                            if (host.description) {
                                props.children('.description').children('.prop-value').text(host.description);
                                props.children('.description').show();
                            } else {
                                props.children('.description').hide();
                            }
                            if (host.is_active) {
                                props.children('.is_active').children('.prop-value').text('да');
                            } else {
                                props.children('.is_active').children('.prop-value').text('нет');
                            }
                            siteDetailInfo.find('.show-access-data').attr('formaction', url);
                            siteDetailInfo.find('.delete-host-form')
                                .attr("action", "/sites/delete/" + host["id"] + "/");


                            siteDetailInfo.fadeIn(200); 
                            return false;

                            modal = $('#site-edit-modal');
                            modal.find('[name|="name"]').val(host.site_name);
                            modal.find('[name|="description"]').val(host.description);
                            modal.find('[name|="domain"]').val(host.domain).attr('disabled', true);
                            if (host.is_active) {
                                modal.find('#id_is_active').attr('checked', true);
                            } else {
                                modal.find('#id_is_active').attr('checked', false);
                            }
                            $(modal).modal();
                        }
                        return false;
                    },
                });
                return false;
            }); 
        }
    },
    hostFilter: {
        search: function(queryString) {
            var sites = $('.site-item-block');
            var mark =  {
                begin: '<span class="mark">',
                end: '</span>'
            };
            var query = {};
            query.raw = queryString.trim();
            query.parsed = query.raw.toUpperCase();

            var domain = {};
            var name = {};
            var matches = 0;

            for (var i = 0; i < sites.length; ++i) {
                found =  false;
                site = $(sites[i]);
                domain.obj = site.find('.filter-domain');
                domain.raw = domain.obj.text(),
                domain.parsed = domain.raw.toUpperCase(),
                name.obj = site.find('.filter-name');
                name.raw = name.obj.text();
                name.parsed = name.raw.toUpperCase();

                domain.obj.html(domain.raw);
                name.obj.html(name.raw);

                domain.match = domain.parsed.indexOf(query.parsed);
                name.match = name.parsed.indexOf(query.parsed);

                if (domain.match !== -1) {
                    mark.content = domain.raw.substring(domain.match, domain.match + query.raw.length);
                    domain.html = domain.raw.substring(0, domain.match) + mark.begin + mark.content + mark.end + domain.raw.substring(domain.match + query.raw.length);
                    domain.obj.html(domain.html) ; 
                    found = true;
                }
                if (name.match !== -1) {
                    mark.content = name.raw.substring(name.match, name.match + query.raw.length);
                    name.html = name.raw.substring(0, name.match) + mark.begin + mark.content + mark.end + name.raw.substring(name.match + query.raw.length);
                    name.obj.html(name.html); 
                    found = true;
                }

                if (found) {
                    ++matches;
                    if (site.is(':hidden')) {
                        site.show();
                    }
                } else {
                    if (!site.is(':hidden')) {
                        site.hide();
                    }
                }
            }
            $('#host-count').text(matches);
            if (matches == 1) {
                sites.each(function(i, site) {
                    if (!$(site).is(':hidden')) {
                        siteLink = $(site).children('a.site-item');
                        if (!siteLink.hasClass('active')) {
                            siteLink.click();
                        }
                        return;
                    }
                });
            }
        },
        init: function() {
            var searchForm = $('.search-form');
            var searchInput = searchForm.find('input[type|="search"]');

            searchForm.bind("submit", function() {
                application.hostFilter.search(searchInput.val());
                searchInput.focus();
                return false;
            });

            searchInput.bind("keyup", function(){
                searchForm.submit();
            });
        }
    },
    modals: {
        init: function() {
            $('.show-access-data').click(function(){
                item = $(this);
                item.addClass('disabled');
                $.ajax({
                    url: item.attr('formaction'), 
                    data: 'private=1',
                    success: function(response) {
                        if (response.success) {
                            buildHostInfoModal(response.data);
                            $('#success-modal').find('h1').text(response.data["domain"]);
                            $('#success-modal').find('p.alert').hide();
                            $('#success-modal').modal();
                        }
                    },
                });
                item.removeClass('disabled');
                return false;
            });  
        }
    },
    ajax: {
        setup: function() {
            ajaxOptions = {
                type: "GET",
                dataType: "json",
                crossDomain: false,
                timeout: 10000,
            }; 
            ajaxOptions.error = function(jqXHR, textStatus, errorThrown) {
                message = "Произошла ошибка при выполнении запроса.";
                message += "\n\n" + jqXHR.status + " "  + errorThrown;
                alert(message);
            };
            $.ajaxSetup(ajaxOptions);
        }
    }
};

function buildHostInfoModal(data) {
    $('#new-domain').text(data["domain"]);
    $('#new-system-user').text(data["username"]);
    $('#new-system-passwd').text(data["password"]);
    $('#new-db-user').text(data["username"]);
    $('#new-db-name').text(data["username"]);
    $('#new-db-passwd').text(data["db_password"]);
    $('#new-system-host').text(data["host"]);
}

$(document).ready(function() {
    application.ajax.setup();
    application.hostAddForm.init();
    application.hostChangeForm.init();
    application.hostDeleteForm.init();
    application.hostList.init();
    application.hostFilter.init();
    application.modals.init();
});