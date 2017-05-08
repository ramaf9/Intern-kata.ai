
class Graph(object):
    """
        Graph class membantu merubah data pada
        repo menjadi berbentuk graph
        dan mencari relasi antar node
    """
    @staticmethod
    def personGraph(repo):
        """
            params: Repo class
            merubah list person dalam bentuk
            graph
        """
        graph = {}
        # looping list person pada class repo
        # mencari relasi tiap node
        for i,c in repo.dictPerson.items():
            node = []
            person = []

            # relasi parent
            a = c.getParents()
            if a:
                for nxt in a:
                    person.append(nxt.getId())

            # relasi pasangan
            a = c.getSpouse()
            if a:
                for nxt in a:
                    person.append(nxt.getId())

            # relasi anak
            a = c.getChildren()
            if a:
                for nxt in a:
                    person.append(nxt.getId())

            # relasi saudara laki2
            a = c.getBrothers()
            if a:
                for nxt in a:
                    person.append(nxt.getId())

            # relasi saudara perempuan
            a = c.getSisters()
            if a:
                for nxt in a:
                    person.append(nxt.getId())

            # add person to graph
            graph[c.getId()] = set(person)
        return graph

    @staticmethod
    def bfs_paths(graph, start, goal):
        """
            params: array, string, string
            mencari dan mengembalikan person
            berdasarkan id
        """
        # set queue
        queue = [(start, [start])]
        # looping queue
        while queue:
            # mengambil satu node
            (vertex, path) = queue.pop(0)
            for next in graph[vertex] - set(path):
                if next == goal:
                    # return value
                    yield path + [next]
                else:
                    queue.append((next, path + [next]))

    @staticmethod
    def getRelationRoot(person1, person2):
        """
            params: person, person
            mencari relasi keturunan dari yang tertua
        """
        person = []
        person.append(person1)
        person_2 = []
        person_2.append(person2)
        new_distance = 0
        value = {}
        value['root'] = None # akar relasi (person)
        value['distance'] = 0 # jarak terjauh tiap lompatan (int)
        count = 0
        new_distance = 0
        new_distance_2 = 0
        # looping untuk tiap person dalam array
        for c in person:
            # simpan variabel person
            current_person = c
            count = count+1
            # loop untuk tiap person2
            for c in person_2:
                # cek apakah person == person2
                if current_person.getId() == c.getId():
                    value['root'] = c # simpan person
                    break
                # cek apakah person2 memiliki orang tua
                if c.getParents() and c.getParents() not in person_2:
                    # menambahkan jarak baru
                    new_distance_2 = new_distance_2 + 1
                    # tambahkan orang tua menjadi bagian dari person2
                    person_2.extend(c.getParents())

            person_2 = [] # set person2 menjadi default
            person_2.append(person2)
            # cek apakah jarak awal lebih kecil dari jarak baru
            if new_distance < new_distance_2:
                # set jarak baru
                value['distance'] = new_distance_2
            else:
                value['distance'] = new_distance

            new_distance_2 = 0 # mengubah nilai awal
            # berhenti bila akar relasi telah ditemukan
            if value['root']:
                break
            # cek apakah person memiliki orang tua
            elif current_person.getParents() and current_person.getParents() not in person:
                # tambahkan orang tua ke dalam person
                person.extend(current_person.getParents())
                # tambahkan jarak
                new_distance = new_distance + 1
        # cek bila memiliki relasi
        if value['root']:
            # cek distance baru
            if value['distance'] < new_distance:
                value['distance'] = new_distance # set distance akhir
            return value
        else:
            return None

    @staticmethod
    def shortest_path(graph, start, goal):
        """
            params: array, string, string
            mencari jalan tercepat dari fungsi bfs
        """
        try:
            return next(Graph.bfs_paths(graph, start, goal))
        except StopIteration:
            return None
