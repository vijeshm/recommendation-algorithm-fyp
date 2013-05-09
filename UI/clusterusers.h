#ifndef CLUSTERUSERS_H
#define CLUSTERUSERS_H

#include <QWidget>
#include <QProcess>

namespace Ui {
class clusterusers;
}

class clusterusers : public QWidget
{
    Q_OBJECT
    
public:
    QProcess *proc;
    QProcess *showproc;
    explicit clusterusers(QWidget *parent = 0);
    ~clusterusers();
    
private:
    Ui::clusterusers *ui;

public slots:
    void movenext();
    void moveback();
    void clusterclick();
    void showclick();
    void showprocended();
    void clusterended();

signals:
    void movetorecommend();
    void movebacktocommputesimilarity();

};

#endif // CLUSTERUSERS_H
