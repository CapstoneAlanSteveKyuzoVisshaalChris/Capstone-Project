class State:

    def __init__(self):
        self.state = 'eyJzZXNzaW9uX2lkIjoiNjc3OGFmYzUtNjExYi00ODQzLWIxMTgtMWRjNjMzZWZiMDg3Iiwic2tpbGxfcmVmZXJlbmNlIjoibWFpbiBza2lsbCIsImFzc2lzdGFudF9pZCI6IjIxMjBkNGI0LTVkMjEtNDg4MC05ODFjLTI0NTQzNmM3ZTEyZiIsImluaXRpYWxpemVkIjp0cnVlLCJkaWFsb2dfc3RhY2siOlt7ImRpYWxvZ19ub2RlIjoiV2VsY29tZSJ9XSwiX25vZGVfb3V0cHV0X21hcCI6eyJXZWxjb21lIjp7IjAiOlswLDBdfX0sImxhc3RfYnJhbmNoX25vZGUiOiJXZWxjb21lIn0='

    def update(self, st):
            self.state = st

    def getState(self):
            return self.state