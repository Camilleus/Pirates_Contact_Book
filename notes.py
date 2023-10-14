
class Note:
    def __init__(self,title:str='Title',note_contents:str='',*tags:str)->None:
        self.title=title
        self.tags=list(tags)+[title]
        self.note_contents=note_contents

    def add_tags(self,*new_tags:str)->None:
        self.tags+=list(new_tags)

    def remove_tags(self,*tags_to_remove:str)->None:
        for tag in tags_to_remove:
            try:
                    self.tags.remove(tag)
            except ValueError as e:
                if str(e) != 'list.remove(x): x not in list':
                    raise ValueError(e)

    def edit_note(self,new_text:str)->None:
        self.note_contents=new_text




