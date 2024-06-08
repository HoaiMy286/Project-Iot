from task import *

class Scheduler:
    TICK = 100 # 100ms
    SCH_MAX_TASKS = 40 # so luong task toi da
    SCH_tasks_G = [] # mang chua cac task
    current_index_task = 0 # index cua task hien tai

    def __int__(self): # ham khoi tao
        # khoi tao cac gia tri ban dau
        self.current_index_task = 0
        self.SCH_tasks_G = []
        return

    def SCH_Init(self): # khoi tao cac gia tri ban dau
        self.current_index_task = 0

    def SCH_Add_Task(self, pFunction, DELAY, PERIOD): # them task vao mang
        if self.current_index_task < self.SCH_MAX_TASKS: # kiem tra xem mang co day chua
            aTask = Task(pFunction, DELAY / self.TICK, PERIOD / self.TICK) # tao task moi
            aTask.TaskID = self.current_index_task # gan id cho task
            self.SCH_tasks_G.append(aTask) # them task vao mang
            self.current_index_task += 1 # tang index len 1
        else:
            print("PrivateTasks are full!!!")

    def SCH_Update(self): # cap nhat cac task
        for i in range(0, len(self.SCH_tasks_G)): # duyet qua tat ca cac task
            if self.SCH_tasks_G[i].Delay > 0: # kiem tra xem task co bi delay khong. Neu co thi giam delay di 1
                self.SCH_tasks_G[i].Delay -= 1 # giam delay di 1
            else: # neu khong thi tang RunMe len 1, runMe la bien de kiem tra xem task co chay hay khong
                self.SCH_tasks_G[i].Delay = self.SCH_tasks_G[i].Period # gan delay = period
                self.SCH_tasks_G[i].RunMe += 1 # tang RunMe len 1

    def SCH_Dispatch_Tasks(self): # chay cac task
        for i in range(0, len(self.SCH_tasks_G)): # duyet qua tat ca cac task
            if self.SCH_tasks_G[i].RunMe > 0: # kiem tra xem task co chay hay khong
                self.SCH_tasks_G[i].RunMe -= 1 # giam RunMe di 1
                self.SCH_tasks_G[i].pTask() # chay task

    def SCH_Delete(self, aTask): # xoa task
        for i in range(0, len(self.SCH_tasks_G)): # duyet qua tat ca cac task
            if self.SCH_tasks_G[i].TaskID == aTask.TaskID: # kiem tra xem task co ton tai trong mang hay khong
                self.SCH_tasks_G.pop(i) # xoa task
                break
        return

    def SCH_GenerateID(self):
        #tao id cho task
        return self.current_index_task