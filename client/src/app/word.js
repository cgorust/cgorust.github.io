class Word {
  add_button(id, text) {
    $('#buttons').append("<span><a \
        class = \"btn btn-success\" \
        role = \"button\" \
        id = \"" + id + "\" \
        >"  
        + text + 
        "</a>&nbsp;</span>");  
  }

  add_word_edit_button()        { 
    this.add_button("word_edit", "Edit"); 
    var self = this
    $('main').on('click', '#word_edit', function(e) {
      e.preventDefault();
      self.create_edit_page();
    });
  }

  add_word_create_button()      { 
    this.add_button("word_create", "Add"); 
    var self = this
    $('main').on('click', '#word_create', function(e) {
      e.preventDefault();
      self.create_create_page();
    });    
  }
  
  add_word_save_button()        { 
    this.add_button("edit_save", "Save"); 
    var self = this
    $('main').on('click', '#edit_save', function(e) {
      e.preventDefault();
      $.ajax({
        type: "POST",
        url: window.location.href, 
        data: $.param({ 
          action: "save", 
          content : $('main').html()
        }),
        success: function(message) {
          console.log(message);
          $('#message').html(message);
        }
      });
    });
  }

  add_done_button()             {
    $('#buttons').append( "<a class=\"btn btn-success\" \
        role=\"button\" href=\"" + window.location.pathname + "\">Done</a> ");  
  }
  
  remove_word_edit_button()     { $('#word_edit').parent().remove(""); }
  remove_word_create_button()   { $('#word_create').parent().remove(""); }
  
  add_message_box() {
    $('#buttons').append( "<div class=\"alert alert-warning\" \
        role=\"alert\" id=\"message\">Server message...</div>");  
  }
  
  make_relations_editable(relation) {
    $( "b:contains('" + relation + "')").siblings().each(function(index) {
      $(this).attr("contentEditable", "true");
    });
    $("b:contains('" + relation + "')").parent().removeAttr("hidden");
    this.add_buttons_of_relation(relation);
  }

  make_page_editable() {
    $('#header').attr("contentEditable", "true");
    $('#word_content').attr("contentEditable", "true");
    $('#word_content').text(this.content);

    this.make_relations_editable("Superconcept");
    this.make_relations_editable("Subconcept");
    this.make_relations_editable("Supercategory");
    this.make_relations_editable("Subcategory");

    this.enable_suggestion();
  }
  
  enable_suggestion() {
    $('body').on('focus', '[contenteditable]', function() {
      const $this = $(this);
      $this.data('before', $this.html());
    }).on('blur keyup paste input', '[contenteditable]', function() {
      const $this = $(this);
      if($this.attr('id') == 'word_content') 
        return;
      if ($this.text() == "") {
        $this.html("&nbsp;&nbsp;&nbsp;");
      }
      if ($this.data('before') !== $this.text()) {
        $this.data('before', $this.text());
        $.ajax({
          type: "POST",
          url: "/suggestion/", 
          data: $this.text(),
          success: function(message) {
            //console.log(typeof message);
            $('#message').html(message);
          }
        });
      }
    });  
  }
  
  add_buttons_of_relation(tag) {
    $("b:contains('" + tag + "')").parent().append(
        " <button class=\"btn btn-success\" id=\"remove_relation"+ tag  + "\" role=\"button\">-</button>\
        <button class=\"btn btn-success\" id=\"add_relation"+ tag  + "\" role=\"button\">+</button>");
    let relations = $("b:contains('" + tag + "')").parent().children("span");
    if(relations.length == 0) {
      $("#remove_relation" + tag).prop('disabled', true);
    }  
    $("#remove_relation" + tag).click(function () {
        let relations = $("b:contains('" + tag + "')").parent().children("span");
        if(relations.length == 0) return;
        if(relations.length == 1) { // remove cannot change length
          $("#remove_relation" + tag).prop('disabled', true);
        }
        relations.last().remove();
    });    
    $("#add_relation" + tag).click(function () {
      let relations = $("b:contains('" + tag + "')").parent().children("span");
      let space = "";
      if(relations.length != 0) space = ", ";
      $( "<span>" + space + "<a contenteditable=\"true\">&emsp;</a></span>").insertBefore("#remove_relation" + tag);
      $("#remove_relation" + tag).prop('disabled', false);
    });    
  }
  
  make_page_addable() {
    $('#header').html(" ");
    $('#word_content').html("");
    $("b:contains('Superconcept')").parent().contents('span').remove();
    $("b:contains('Subconcept')").parent().contents('span').remove();
    $("b:contains('Supercategory')").parent().contents('span').remove();
    $("b:contains('Subcategory')").parent().contents('span').remove();
    this.make_page_editable()
    $('#word_content').html("");
    this.enable_suggestion();
  }
  
  create_edit_page() {
    this.remove_word_edit_button();
    this.remove_word_create_button();
    this.add_word_save_button();
    this.add_done_button();
    this.add_message_box();
    this.make_page_editable();
  }
  
  create_create_page() {
    this.remove_word_edit_button();
    this.remove_word_create_button();
    this.add_word_save_button();
    this.add_done_button();
    this.add_message_box();
    this.make_page_addable();
  }
  
  is_local_word_page() {
    if (location.hostname !== "localhost" && location.hostname !== "127.0.0.1") 
      return false;
    if(!window.location.pathname.includes("/dictionary/")) 
      return false;
    return true;
  }

  constructor() {
    if(!this.is_local_word_page())
      return;
    this.content = $('#word_content').text()
    this.add_word_edit_button();
    this.add_word_create_button();
  }
}	

export { Word };

if (false) {
  let word = new Word();
}
