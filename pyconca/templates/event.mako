<%inherit file="pyconca:templates/base.mako"/>

<%block name="content">

<div class="row-fluid">
  <div class="span12 sub-header-container">
    <div class="row-fluid sub-header-image">
      <div class="span12 top-row">
        <h1 class="header-main-text"><%block name="title"/></h1>
        <h2 class="header-sub-text">PyCon Canada 2012</h2>
        <h2 class="header-sub-text">Toronto, November 9th - 11th</h2>
      </div>
    </div>
  </div>
</div>

<div class="row-fluid">
  <div class="content-holder">
    <div class="row-fluid">

      <div class="span3">
        <h3>Quick Links</h3>
        <ul id="sidenav" class="sidenav side-block"></ul>

        <h3>Sponsors</h3>
        <div id="sponsors_carousel" class="carousel slide side-block">
          <div class="carousel-inner">
            <div class="active item">
             <img src="${request.static_url("pyconca:static/vmfarms-logo.png")}"
                  width="200px;" height="100px;" alt="">
             <br>
             <img src="${request.static_url("pyconca:static/freshbooks.gif")}"
                  width="200px;" height="100px;" alt="">
            </div>
            <div class="item">
             <img src="${request.static_url("pyconca:static/vmfarms-logo.png")}"
                  width="200px;" height="100px;" alt="">
             <br>
             <img src="${request.static_url("pyconca:static/freshbooks.gif")}"
                  width="200px;" height="100px;" alt="">
            </div>
          </div>
        </div>
      </div>

      <div class="span9 content-column">
        <%block name="info"/>
      </div>
    </div>
  </div>
</div>

<script>
  function createSidenav() {
    $(".header").each(function() {
      var $this = $(this);
      var navItemHolder = $("<li></li>");
      var navItem = $("<a></a>");

      if (!$this.attr("id")) {
        var anchor = $this.text()
          .toLowerCase()
          .replace(/ /g, "-")
          .replace(/[^a-z0-9-]/g, "");
        $this.attr("id", anchor);
      }

      navItem
        .text($this.text())
        .addClass("sidenav-link btn")
        .attr("href", "#" + $this.attr("id"));

      navItemHolder
        .append(navItem)
        .addClass("sidenav-item");

      $("#sidenav").append(navItemHolder);
    });
  };

  $(function() {
    createSidenav();
    $('.carousel').carousel({
      interval: 3000
    });
  });
</script>

</%block>
