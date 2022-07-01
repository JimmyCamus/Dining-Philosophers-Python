import threading
import time


class Philosopher(threading.Thread):
    diner_acc = 0

    def __init__(self, index, left_fork, right_fork):
        threading.Thread.__init__(self)
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while self.diner_acc < 10:
            # Philosopher is thinking.
            time.sleep(3)
            print("Philosopher %s is hungry." % (self.index + 1))
            self.dine()

    def dine(self):
        # if both the forks are free, then philosopher will eat.
        left_fork, right_fork = self.left_fork, self.right_fork
        while self.diner_acc < 10:
            left_fork.acquire()  # wait operation on left fork.
            locked = right_fork.acquire(False)
            if locked:
                break  # if right fork is not available leave left fork.
            left_fork.release()
            print("Philosopher %s swaps forks." % (self.index + 1))
            left_fork, right_fork = right_fork, left_fork
        else:
            return
        self.dining()
        # release both the fork after dining.
        right_fork.release()
        left_fork.release()

    def dining(self):
        print("Philosopher %s starts eating." % (self.index + 1))
        # Philosopher is eating for 3 seconds.
        time.sleep(3)
        print("Philosopher %s finishes eating and leaves to think." % (self.index + 1))
        self.diner_acc += 1


def main():
    philosophers_cuantity = 50
    # initialising array of semaphore of forks.
    forks = [threading.Semaphore() for n in range(philosophers_cuantity)]

    # here (i+1)%philosophers_cuantity is used to get right and left forks circularly between 1 - philosophers_cuantity.
    philosophers = [
        Philosopher(
            i, forks[i % philosophers_cuantity], forks[(i + 1) % philosophers_cuantity]
        )
        for i in range(philosophers_cuantity)
    ]

    for p in philosophers:
        p.start()


if __name__ == "__main__":
    main()
