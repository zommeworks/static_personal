import sys
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
#import matplotlib.pyploy as plt
import numpy as np
import transformation

def get_tf_matrix(sensor_pose):
    #print(self.sensor_pose)
    translation = sensor_pose[:3]
    euler = sensor_pose[3:]
    #print(euler)
    tf_matrix = transformation.euler_matrix(*euler)
    tf_matrix[:3, 3] = translation
    return tf_matrix


def step(acc_x, acc_y, acc_z, roll, pitch, yaw, dt):
    tf_matrix = get_tf_matrix(sensor_pose=[0,0,0, roll, pitch, yaw])
    transformed = np.matmul(tf_matrix, np.array([[acc_x, 0, 0, 1], [0, acc_y, 0, 1], [0,0,acc_z,1]]).T )
    acc_X = transformed[0,:].sum()
    acc_Y = transformed[1,:].sum()
    acc_Z = transformed[2,:].sum()    # 월드 좌표계 기준으로 변환된 가속도, 셋중에 하나는 -9.8 or이어야할 것(그게 Z축)
                                # 나머지 두 좌표축 확인해서 계산에 적절하게 사용

    return acc_X, acc_Y, acc_Z


def read_file():
    print('>>> following csv files are found: ')
    filenames = os.listdir('data/')
    for filenametemp in filenames:
        print (filenametemp)

    filename = input('>>> enter filename in data directory: ')
    filename = re.sub('.csv', '', filename)
    print(filename)

    if os.path.isfile("data/" + filename + ".csv") or os.path.isfile("data/" + filename + '.csv'):
        print('>>> successfully read ' + filename + '.csv')
        ds = pd.read_csv('data/' + filename + '.csv')
        return filename, ds
    else:
        print('>>> wrong name. please try again.')
        return False

def draw_plot(name, axis, v1, v2):
    plt.scatter(v1, v2)
    plt.savefig('output/position_'+name+'_'+axis+'.png')
    plt.clf()

def main():
    read_data = read_file()
    df = pd.DataFrame(columns = ['Timestamp', 'pose_X', 'pose_Y', 'pose_Z', 'acc_X', 'acc_Y', 'acc_Z', 'roll', 'pitch', 'yaw'])
    pose_X = 0
    pose_Y = 0
    pose_Z = 0
    v_X = 0
    v_Y = 0
    v_Z = 0

    
    for i in range(len(read_data[1])-1):
        dt = 0.01
        acc_x, acc_y, acc_z = read_data[1]['accelX'][i]*9.8, read_data[1]['accelY'][i]*9.8, read_data[1]['accelZ'][i]*9.8   # [m/s^2] 얻은 데이터가 9.8m/s^2 => 1로 스케일된 데이터였음에 주의
        roll, pitch, yaw = read_data[1]['Roll(rads)'][i], read_data[1]['Pitch(rads)'][i], read_data[1]['Yaw(rads)'][i]    # [radian]

        acc_X, acc_Y, acc_Z = step(acc_x, acc_y, acc_z, roll, pitch, yaw, dt)
        v_X = v_X + acc_X*dt
        v_Y = v_Y + acc_Y*dt
        v_Z = v_Z + acc_Z*dt

        if i != 0:
            pose_X = pose_X + v_X*dt
            pose_Y = pose_Y + v_Y*dt
            pose_Z = pose_Z + v_Z*dt
        
        if i%10 == 0:
            ni = i//10
            df.loc[ni] = [read_data[1]['Timestamp'][ni], pose_X, pose_Y, pose_Z, acc_X, acc_Y, acc_Z, roll, pitch, yaw]

    print(df)
    df.to_csv('output/out_' + read_data[0] + '.csv', index=False)

    draw_plot(read_data[0], 'xy', df['pose_X'], df['pose_Y'])
    draw_plot(read_data[0], 'yz', df['pose_Y'], df['pose_Z'])
    draw_plot(read_data[0], 'zx', df['pose_Z'], df['pose_X'])
    
    print('>>> out_'+read_data[0]+'.csv has been exported.')
    print('>>> end of process')

if __name__ == '__main__':
    main()
