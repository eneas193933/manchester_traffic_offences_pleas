

class MultiStageForm(object):
    def __init__(self, current_stage, url_name, storage_dict):
        self.urls = OrderedDict()
        self.current_stage_class = None
        self.current_stage = None
        self.storage_dict = storage_dict
        self.request_context = {}
        self.all_data = {}
        self.url_name = url_name

        for stage_class in self.stage_classes:
            self.urls[stage_class.name] = reverse(url_name, args=(stage_class.name,))
            self.all_data[stage_class.name] = {}
            if stage_class.name == current_stage:
                self.current_stage_class = stage_class

        self.load_from_storage(storage_dict)

        if self.current_stage_class is None:
            raise Http404

    def _get_stage_class(self, name):
        for stage_class in self.stage_classes:
            if stage_class.name == name:
                return stage_class

    def load_from_storage(self, storage_dict):
        # copy data out so we're not manipulating an external object
        self.all_data.update({key: val for (key, val) in storage_dict.items()})

    def save_to_storage(self):
        self.storage_dict.update({key: val for (key, val) in self.all_data.items()})

    def load(self, request_context):
        self.request_context = request_context
        self.current_stage = self.current_stage_class(self.urls, self.all_data)

        if not self.current_stage.check_dependencies():
            return HttpResponseRedirect(self.urls[self.stage_classes[0].name])

        self.current_stage.load(request_context)

    def save(self, form_data, request_context, next_step=None):
        self.request_context = request_context
        next_url = None
        if next_step:
            next_url = reverse(self.url_name, args=(next_step, ))

        self.current_stage = self.current_stage_class(self.urls, self.all_data)
        if self.current_stage.name not in self.all_data:
            self.all_data[self.current_stage.name] = {}

        self.all_data[self.current_stage.name].update(self.current_stage.save(form_data, next_step=next_url))
        self.save_to_storage()

        return True

    def process_messages(self, request):
        if self.current_stage is None:
            raise Exception("Current stage is not set")

        for msg in self.current_stage.messages:
            messages.add_message(request, msg.importance, msg.message, extra_tags=msg.tags)

    def render(self):
        return self.current_stage.render(self.request_context)