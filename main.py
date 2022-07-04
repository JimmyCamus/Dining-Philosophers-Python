import threading
import time
class Philosopher(threading.Thread):
    diner_acc = 0

    def __init__(self, index, left_fork, right_fork):
        """This fuction is the constructor of the class 

        Args:
            index (int): number of the philosopher 
            left_fork (semaphore): left philosopher's fork
            right_fork (semaphore): right philosopher's fork
        """
        threading.Thread.__init__(self)
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        """This function make the "dinner" begins
        """
        while self.diner_acc < 10:
            # Philosopher is thinking.
            time.sleep(3)
            print("Philosopher %s is hungry." % (self.index + 1))
            self.dine()

    def dine(self):
        """This functions defines the logic of the "dinner" 
        """
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
        self.dinning()
        # release both the fork after dinning.
        right_fork.release()
        left_fork.release()

    def dinning(self):
        """This function defines the time while the philosopher is dinning (3)
        """
        print("Philosopher %s starts eating." % (self.index + 1))
        # Philosopher is eating for 3 seconds.
        time.sleep(3)
        print("Philosopher %s finishes eating and leaves to think." % (self.index + 1))
        self.diner_acc += 1


def main():
    """This function is the main of the code and call the another functions and create the philosophers
    """
    philosophers_cuantity = 10
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
